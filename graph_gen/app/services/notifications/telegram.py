from datetime import datetime

import requests
from pydantic import BaseModel

from app.services.log_parser import get_unique_vlans
from app.services.notifications.builder import NotificationBuilder


class ChatSchema(BaseModel):
    id: int


class TelegramNotificationSchema(BaseModel):
    token: str
    chats: list[ChatSchema]


class TelegramNotificationBuilder(NotificationBuilder):

    def _build_notification_message(self) -> str:
        vlans = get_unique_vlans(self.records)
        vlans_text = "\n".join(
            [f"🌐 VLAN {vid} ({self.get_vlan_name(vid)}) в кол-ве {count}" for vid, count in vlans.items()]
        )

        return f"""
❗️Замечена петля на сети❗️
🗓 {datetime.now().strftime('%d %B %Y %H:%M')}

Количество сообщений: {len(self.records)}
{vlans_text}
Оборудование:
{'\n'.join(self.devices)}
        """


class TelegramNotification:

    def __init__(self, bots: list[TelegramNotificationSchema], builder: NotificationBuilder):
        self._bots = bots
        self._builder = builder

    def notify_all(self):
        for bot in self._bots:
            for chat in bot.chats:
                self._send_message(bot.token, chat.id)

    def _send_message(self, token: str, chat_id: int):
        data = {"chat_id": chat_id, "text": self._builder.build_notification_message()}
        response = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=3)
        if response.status_code == 200:
            print(f"Message sent to chat {chat_id}")
        else:
            print(f"Failed to send message to chat {chat_id}")
