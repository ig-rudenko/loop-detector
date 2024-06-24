import json
from datetime import datetime
from pathlib import Path

from app.services.cache import get_cache
from app.services.log_parser import Record
from app.settings import settings


class LogsRecorder:

    def __init__(self, logs_records: list[Record]):
        self.new_logs_records = logs_records
        self.has_new_logs = len(self.new_logs_records) > 0

        self._cache = get_cache()
        self._cache_timeout = settings.cache_timeout

        self._logs_cache_key = "loop_detected_records"
        self._loop_name = self.get_loop_name()

    def get_all_logs_records(self) -> list[Record]:
        # Получаем прошлые логи из кеша.
        past_logs_records: list[Record] = self._cache.get(self._logs_cache_key) or []
        all_records = past_logs_records + self.new_logs_records
        return all_records

    def save(self):
        all_logs_records = self.get_all_logs_records()
        self._save_to_cache(all_logs_records)
        self._save_to_file(all_logs_records)

    def _save_to_cache(self, all_logs_records: list[Record]):
        if self.has_new_logs:
            # Если есть новые логи, то добавляем их в Redis, чтобы их можно было использовать в будущем.
            # Спустя `timeout` данные логи будут удалены из Redis.
            self._cache.set(self._logs_cache_key, value=all_logs_records, timeout=self._cache_timeout)

    def _save_to_file(self, records: list[Record]):
        if self.has_new_logs:
            storage_path = Path(settings.storage)
            storage_path.mkdir(parents=True, exist_ok=True)
            with (storage_path / f"{self._loop_name}_messages.json").open(mode="w") as file:
                json.dump(records, file)

    def get_loop_name(self):
        cache_key = "current_loop_name"
        cached_name: str | None = self._cache.get(cache_key)
        if cached_name is None:
            name = f"loop_{datetime.now().strftime('%d.%m.%Y_%H.%M')}"
            self._cache.set(cache_key, value=name, timeout=self._cache_timeout)
        else:
            name = cached_name
        return name
