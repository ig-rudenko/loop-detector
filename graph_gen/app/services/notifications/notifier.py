import json
from pathlib import Path
from typing import Callable

from loguru import logger
from pydantic import ValidationError

from app.graph import Node
from app.services.log_parser import Record
from app.services.notifications.telegram import (
    TelegramNotificationSchema,
    TelegramNotificationBuilder,
    TelegramNotification,
)
from app.settings import settings


def notify(*, records: list[Record], nodes: list[Node], get_vlan_name: Callable[[int], str] = lambda x: ""):
    """
    Отправка уведомлений обнаружения петель на сети.
    """

    if len(records) <= settings.records_count_notification_limit:
        # Если количество уведомлений НЕ превышает лимит, то не отправляем.
        return

    try:
        with open(Path(settings.notifications_config), encoding="utf-8") as f:
            config = json.load(f)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as exc:
        logger.error(f"Invalid notifications config: {exc}")
        return

    # Через телеграм ботов.
    if config.get("telegram") and isinstance(config["telegram"], list):
        try:
            bots_config = [
                TelegramNotificationSchema.model_validate(bot_config) for bot_config in config["telegram"]
            ]
        except ValidationError:
            logger.error(f"Invalid telegram config: {config['telegram']}")
            return

        builder = TelegramNotificationBuilder(
            records=records, devices=[f"{d.name} ({d.ip})" for d in nodes], get_vlan_name=get_vlan_name
        )
        notification = TelegramNotification(bots_config, builder)
        notification.notify_all()
