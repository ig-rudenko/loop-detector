import json
from pathlib import Path

from app.schemas.log_messages import LogMessageSchema
from app.services.cache import get_cache
from app.settings import settings


async def get_current_log_messages() -> list[LogMessageSchema]:
    cache = get_cache()
    data = await cache.get('loop_detected_records') or []
    return [LogMessageSchema(**record) for record in data]


async def delete_current_log_messages() -> None:
    cache = get_cache()
    await cache.delete('loop_detected_records')


def get_stored_log_messages(loop_name: str) -> list[LogMessageSchema]:
    if not loop_name.endswith("_messages"):
        loop_name += "_messages"

    for file in Path(settings.graph_storage).glob("*.json"):
        if file.name.startswith(loop_name):
            try:
                with file.open('rb') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                continue
            else:
                return [LogMessageSchema(**record) for record in data]

    return []
