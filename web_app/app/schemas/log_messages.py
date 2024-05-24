from pydantic import BaseModel, Field


class HostSchema(BaseModel):
    ip: str


class LogMessageSchema(BaseModel):
    timestamp: str = Field(..., alias="@timestamp")
    message: str
    host: HostSchema
