from pydantic import BaseModel, Field


class NodeFontSchema(BaseModel):
    color: str


class NodeSchema(BaseModel):
    id: str
    title: str
    label: str
    shape: str
    color: str
    size: float | int
    font: NodeFontSchema


class EdgeMessageSchema(BaseModel):
    message: str
    timestamp: str


class EdgeSchema(BaseModel):
    id: str
    from_: str = Field(..., alias="from")
    to: str
    value: int | float
    title: str
    messages: list[EdgeMessageSchema]


class GraphSchema(BaseModel):
    nodes: list[NodeSchema]
    edges: list[EdgeSchema]
