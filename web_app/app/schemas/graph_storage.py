from datetime import datetime

from pydantic import BaseModel


class GraphStorageFileSchema(BaseModel):
    name: str
    modTime: datetime
