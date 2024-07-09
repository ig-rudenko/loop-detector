from app.schemas.log_messages import LogMessageSchema
from app.services.cache import get_cache
from app.services.graph_storage import GraphStorage
from app.settings import settings


async def get_current_log_messages() -> list[LogMessageSchema]:
    cache = get_cache()
    data = await cache.get('loop_detected_records') or []
    return [LogMessageSchema(**record) for record in data]


async def delete_current_log_messages() -> None:
    cache = get_cache()
    await cache.delete('loop_detected_records')


def get_stored_log_messages(loop_name: str) -> list[LogMessageSchema]:
    storage = GraphStorage(settings.graph_storage)
    messages = storage.get_storage_messages(loop_name)
    return [LogMessageSchema(**record) for record in messages]
