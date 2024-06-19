from pydantic import BaseModel


class TelegramBotInfo(BaseModel):
    id: int
    first_name: str
    username: str
