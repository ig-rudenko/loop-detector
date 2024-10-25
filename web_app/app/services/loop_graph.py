from loguru import logger

from app.schemas.graph import GraphSchema
from app.services.cache import get_cache


class GraphException(Exception):
    def __init__(self, message: str):
        self.message = message


async def get_current_loop(depth: int = 1) -> GraphSchema:
    """
    Возвращает текущую имеющуюся петлю из кеша в виде графа на основе глубины графа
    :param depth: Глубина графа.
    :return: Схема графа.
    :raises GraphException: Неверный формат данных для графа в кэше
    """
    cache = get_cache()
    key = f"currentLoop:depth={depth}"
    data: dict | None = await cache.get(key)
    if data is not None:
        try:
            return GraphSchema.model_validate(data)
        except ValueError as e:
            logger.error(f"Неверный формат данных для графа в кэше: {e}")
            raise GraphException("Неверный формат данных для графа в кэше")

    return GraphSchema(edges=[], nodes=[])
