import json

from pydantic import BaseModel, Field

from app.services.decorators import singleton
from app.settings import settings


class _Chats(BaseModel):
    id: int
    name: str
    description: str


class _TelegramNotification(BaseModel):
    name: str
    description: str
    token: str
    chats: list[_Chats]


class _NotificationConfig(BaseModel):
    telegram: list[_TelegramNotification] = Field(default_factory=list)


@singleton
class NotificationsConfig:

    class NotFoundError(Exception):
        def __init__(self, detail: str) -> None:
            self.detail = detail

    def __init__(self, config_file_path: str | None = None):
        if config_file_path is None:
            self._config_file_path: str = settings.notifications_conf_file
        else:
            self._config_file_path = config_file_path

        self._config = self._load_config()

    def get_telegram_notifications(self) -> list[_TelegramNotification]:
        return self._config.telegram

    def add_telegram_notification(self, *, name: str, token: str, description: str = ""):
        self._config.telegram.append(
            _TelegramNotification(
                name=name,
                token=token,
                description=description,
                chats=[],
            )
        )
        self._save_config()

    def get_telegram_notification(self, notification_name: str) -> _TelegramNotification:
        for notification in self._config.telegram:
            if notification.name == notification_name:
                return notification
        raise NotificationsConfig.NotFoundError(f"Notification with name {notification_name} not found")

    def update_telegram_notification(
        self,
        notification_name: str,
        *,
        new_name: str | None = None,
        token: str | None = None,
        description: str | None = None,
    ):
        for notification in self._config.telegram:
            if notification.name == notification_name:
                if new_name is not None:
                    notification.name = new_name
                if token is not None:
                    notification.token = token
                if description is not None:
                    notification.description = description
                self._save_config()
                return
        raise NotificationsConfig.NotFoundError(f"Notification with name {notification_name} not found")

    def delete_telegram_notification(self, notification_name: str):
        for notification in self._config.telegram:
            if notification.name == notification_name:
                self._config.telegram.remove(notification)
                self._save_config()
                return
        raise NotificationsConfig.NotFoundError(f"Notification with name {notification_name} not found")

    def add_chat_to_telegram_notification(
        self, notification_name: str, *, chat_id: int, chat_name: str, description: str = ""
    ):
        for notification in self._config.telegram:
            if notification.name == notification_name:
                notification.chats.append(
                    _Chats(
                        id=chat_id,
                        name=chat_name,
                        description=description,
                    )
                )
                self._save_config()
                return
        raise NotificationsConfig.NotFoundError(f"Notification with name {notification_name} not found")

    def update_chat_to_telegram_notification(
        self,
        notification_name: str,
        *,
        chat_id: int,
        chat_name: str | None = None,
        description: str | None = None,
    ):
        for notification in self._config.telegram:
            if notification.name == notification_name:
                for chat in notification.chats:
                    if chat.id == chat_id:
                        if chat_name is not None:
                            chat.name = chat_name
                        if description is not None:
                            chat.description = description
                        self._save_config()
                        return
                raise NotificationsConfig.NotFoundError(
                    f"Chat with id {chat_id} not found in notification {notification_name}"
                )
        raise NotificationsConfig.NotFoundError(f"Notification with name {notification_name} not found")

    def delete_chat_from_telegram_notification(self, notification_name: str, chat_id: int):
        for notification in self._config.telegram:
            if notification.name == notification_name:
                for chat in notification.chats:
                    if chat.id == chat_id:
                        notification.chats.remove(chat)
                        self._save_config()
                        return
                raise NotificationsConfig.NotFoundError(
                    f"Chat with id {chat_id} not found in notification {notification_name}"
                )
        raise NotificationsConfig.NotFoundError(f"Notification with name {notification_name} not found")

    def _load_config(self):
        try:
            with open(self._config_file_path, "r", encoding="utf-8", errors="ignore") as file:
                return _NotificationConfig.model_validate_json(file.read())
        except (FileNotFoundError, PermissionError, json.JSONDecodeError):
            return _NotificationConfig()

    def _save_config(self):
        with open(self._config_file_path, "w", encoding="utf-8") as file:
            file.write(self._config.model_dump_json(indent=2))
