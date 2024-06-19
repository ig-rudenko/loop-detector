from pydantic import BaseModel, Field


class NotificationSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field("", max_length=1024)


class ChatSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field("", max_length=1024)


class TelegramBotNotificationSchema(NotificationSchema):
    chats: list[ChatSchema]


class CreateTelegramBotNotificationSchema(NotificationSchema):
    token: str = Field(..., min_length=40, max_length=255)


class UpdateChatSchema(BaseModel):
    name: str = Field(None, min_length=3, max_length=255)
    description: str = Field(None, max_length=1024)


class UpdateTelegramBotNotificationSchema(BaseModel):
    name: str = Field(None, min_length=3, max_length=255)
    description: str = Field(None, max_length=1024)
    token: str = Field(None, min_length=40, max_length=255)
