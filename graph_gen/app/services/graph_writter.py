import json
from pathlib import Path

from app.settings import settings


def write_graph(graph, loop_name: str):
    """Сохраняет граф в json файл"""
    storage_path = Path(settings.storage)
    storage_path.mkdir(parents=True, exist_ok=True)
    file = storage_path / f"{loop_name}.json"
    with file.open(mode="w", encoding="utf-8") as f:
        json.dump(graph, f, indent=4, ensure_ascii=False)
