import logging
import pickle
from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Any, Optional, TypedDict

from redis.client import Redis

from app.services.decorators import singleton
from app.settings import settings

logger = logging.getLogger(__name__)


class AbstractCache(ABC):
    """Абстрактный класс для реализации кеша данных."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Получает значение из кеша по ключу."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, timeout: int) -> None:
        """Записывает значение в кеш по ключу и устанавливает таймаут для удаления."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Удаляет значение из кеша по ключу."""
        pass

    @abstractmethod
    def delete_namespace(self, prefix: str) -> None:
        """Удаляет все ключи с указанным префиксом"""
        pass


class _ValueType(TypedDict):
    data: Any
    expires: datetime


@singleton
class InMemoryCache(AbstractCache):
    """Кэш данных в памяти."""

    def __init__(self) -> None:
        self._cache: dict[str, _ValueType] = {}

    def get(self, key: str) -> Optional[Any]:
        logger.debug("Get from cache %s", key)

        if value := self._cache.get(key, None):
            if value["expires"] > datetime.now():
                return pickle.loads(value["data"])
            else:
                self.delete(key)
        return None

    def set(self, key: str, value: Any, timeout: int) -> None:
        logger.debug("Set to cache %s", key)

        self._cache[key] = {
            "data": pickle.dumps(value),
            "expires": datetime.now() + timedelta(seconds=timeout),
        }

    def delete(self, key: str) -> None:
        logger.debug("Delete_ from cache %s", key)
        self._cache.pop(key, None)

    def delete_namespace(self, prefix: str) -> None:
        logger.debug("Delete namespace from cache %s", prefix)
        for key in list(self._cache.keys()):
            if key.startswith(prefix):
                self._cache.pop(key, None)


@singleton
class RedisCache(AbstractCache):
    """Кэш данных в Redis."""

    def __init__(self, host: str, port: int, db: int, password: Optional[str] = None) -> None:
        self._redis: Redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            socket_timeout=2,
            socket_connect_timeout=2,
        )

    def get(self, key: str) -> Optional[Any]:
        logger.debug("Get from cache %s", key)

        value: Any = self._redis.get(key)
        if value is not None:
            return pickle.loads(value)
        return None

    def set(self, key: str, value: Any, timeout: int) -> None:
        logger.debug("Set to cache %s", key)
        self._redis.set(key, pickle.dumps(value), ex=timeout)

    def delete(self, key: str) -> None:
        logger.debug("Delete_ from cache %s", key)
        self._redis.delete(key)

    def clear(self) -> None:
        logger.debug("Clear cache")
        self._redis.flushdb(asynchronous=False)

    def delete_namespace(self, prefix: str) -> None:
        logger.debug("Delete namespace from cache %s", prefix)
        for key in self._redis.scan_iter(f"{prefix}*"):
            self._redis.delete(key)


def get_cache() -> AbstractCache:
    """Возвращает кэш в зависимости от настроек приложения"""
    if settings.redis_host:
        return RedisCache(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
        )
    else:
        return InMemoryCache()
