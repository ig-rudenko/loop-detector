from app.schemas.graph_info import GraphInfoSchema, VlanInfoSchema
from app.services.graph_storage import GraphStorage
from app.settings import settings


def get_graph_info(graph_name: str) -> GraphInfoSchema:
    storage = GraphStorage(settings.graph_storage)
    info = storage.get_storage_graph_info(graph_name)
    print(info)

    vlans = []
    for vid, count in info.get("vlans", {}).items():
        vlans.append(VlanInfoSchema(vid=vid, count=count))

    return GraphInfoSchema(vlans=vlans, messagesCount=info["messages_count"])
