import json
from pathlib import Path

from app.settings import settings


def write_graph(graph, loop_name: str):
    """Сохраняет граф в json файл"""
    with (Path(settings.storage) / f"{loop_name}.json").open(mode='w') as f:
        json.dump(graph, f)
