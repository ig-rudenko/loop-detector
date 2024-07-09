from abc import ABC, abstractmethod
from typing import Callable

from app.services.log_parser import Record


class NotificationBuilder(ABC):

    def __init__(
        self, records: list[Record], devices: list[str], get_vlan_name: Callable[[int], str] = lambda x: ""
    ):
        self.records = records
        self.devices = devices
        self.get_vlan_name = get_vlan_name

    def build_notification_message(self, *args, **kwargs) -> str:
        return self._build_notification_message()

    @abstractmethod
    def _build_notification_message(self) -> str:
        pass
