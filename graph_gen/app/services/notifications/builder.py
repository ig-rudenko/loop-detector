from abc import ABC, abstractmethod


class NotificationBuilder(ABC):

    def __init__(self, records_count: int, devices: list[str]):
        self.records_count = records_count
        self.devices = devices

    def build_notification_message(self, *args, **kwargs) -> str:
        return self._build_notification_message()

    @abstractmethod
    def _build_notification_message(self) -> str:
        pass
