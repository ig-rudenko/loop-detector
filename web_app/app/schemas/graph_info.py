from pydantic import BaseModel


class VlanInfoSchema(BaseModel):
    vid: int
    count: int


class GraphInfoSchema(BaseModel):
    messagesCount: int
    vlans: list[VlanInfoSchema]
