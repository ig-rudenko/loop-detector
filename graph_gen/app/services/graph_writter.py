import json

from app.settings import settings


def write_graph(graph, loop_name: str):
    """Сохраняет граф в json файл"""
    settings.storage_path.mkdir(parents=True, exist_ok=True)
    file = settings.storage_path / f"{loop_name}.json"
    with file.open(mode="w", encoding="utf-8") as f:
        json.dump(graph, f, indent=4, ensure_ascii=False)
