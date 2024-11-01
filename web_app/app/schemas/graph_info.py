from pydantic import BaseModel

from app.schemas.graph_storage import GraphStorageFileSchema


class VlanInfoSchema(BaseModel):
    vid: int
    count: int


class GraphInfoSchema(BaseModel):
    messagesCount: int
    vlans: list[VlanInfoSchema]


class GraphsHistoryInfoSchema(GraphStorageFileSchema):
    info: GraphInfoSchema


class PaginatedGraphsHistoryInfoSchema(BaseModel):
    count: int
    results: list[GraphsHistoryInfoSchema]
