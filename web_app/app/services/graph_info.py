from app.schemas.graph_info import (
    GraphInfoSchema,
    VlanInfoSchema,
    GraphsHistoryInfoSchema,
    PaginatedGraphsHistoryInfoSchema,
)
from app.schemas.graph_storage import GraphStorageFileSchema
from app.services.cache import get_cache
from app.services.graph_storage import GraphStorage
from app.settings import settings


async def get_graph_info(graph_name: str, storage: GraphStorage) -> GraphInfoSchema:
    try:
        info = await storage.get_storage_graph_info(graph_name)
    except GraphStorage.GraphStorageException:
        info = {"messages_count": 0}

    vlans = []
    for vid, count in info.get("vlans", {}).items():
        vlans.append(VlanInfoSchema(vid=vid, count=count))

    return GraphInfoSchema(vlans=vlans, messagesCount=info["messages_count"])


async def get_stored_graphs_info(part: int, limit: int) -> PaginatedGraphsHistoryInfoSchema:
    storage = GraphStorage(settings.graph_storage)
    files, total_count = storage.get_part_storage_files(part, limit)

    results = []

    for file in files:
        file.name = file.name.removesuffix(".json")

        results.append(
            GraphsHistoryInfoSchema(
                name=file.name,
                modTime=file.modTime,
                info=await get_graph_info(file.name, storage),
            )
        )
    return PaginatedGraphsHistoryInfoSchema(
        count=total_count,
        results=results,
    )


async def get_stored_graphs_history() -> list[GraphStorageFileSchema]:
    cache_key = "graphs_history"
    cache_timeout = 60 * 5
    cache = get_cache()

    data: list[GraphStorageFileSchema] = await cache.get(cache_key)
    if data is None:
        storage = GraphStorage(settings.graph_storage)
        data, total_count = storage.get_part_storage_files(limit=-1)
        for file in data:
            file.name = file.name.removesuffix(".json")
        await cache.set(cache_key, data, timeout=cache_timeout)

    return data
