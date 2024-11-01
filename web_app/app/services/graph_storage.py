import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import aiofiles

from app.schemas.graph import GraphSchema
from app.schemas.graph_storage import GraphStorageFileSchema


class GraphInfo(TypedDict):
    vlans: dict[int, int]
    messages_count: int


class GraphStorage:
    class GraphStorageException(Exception):
        def __init__(self, message: str):
            self.message = message

    def __init__(self, graph_storage_dir: Path | str):
        self._graph_storage_dir: Path = Path(graph_storage_dir)

    def get_part_storage_files(
        self, part: int = 1, limit: int = 25
    ) -> tuple[list[GraphStorageFileSchema], int]:
        """
        Возвращает список файлов, содержащих информацию о графах.
        :param part: Номер части данных.
        :param limit: Ограничение на количество файлов, если значение меньше 0, то возвращает все файлы.
        """
        try:
            all_files = [
                f
                for f in self._graph_storage_dir.iterdir()
                if f.is_file()
                and f.suffix == ".json"
                and f.name.startswith("loop_")
                and not (f.name.endswith("_messages.json") or f.name.endswith("_info.json"))
            ]
        except FileNotFoundError:
            raise GraphStorage.GraphStorageException(
                f"Graph storage directory not found: `{self._graph_storage_dir}`"
            )
        count = len(all_files)
        sorted_files = sorted(all_files, key=lambda f: f.stat().st_mtime, reverse=True)

        if limit > 0:
            start = (part - 1) * limit
            end = start + limit
            try:
                sorted_files = sorted_files[start:end]
            except IndexError:
                sorted_files = []

        result = [
            GraphStorageFileSchema(name=f.name, modTime=datetime.fromtimestamp(f.stat().st_mtime))
            for f in sorted_files
        ]
        return result, count

    async def get_storage_file(self, name: str) -> GraphSchema:
        try:
            async with aiofiles.open(self._graph_storage_dir / f"{name}.json") as f:
                return GraphSchema.model_validate_json(await f.read())
        except (OSError, json.JSONDecodeError):
            raise GraphStorage.GraphStorageException(f"Failed to load file {name}")

    async def get_storage_graph_info(self, name: str) -> GraphInfo:
        try:
            async with aiofiles.open(self._graph_storage_dir / f"{name}_info.json") as f:
                return json.loads(await f.read())
        except (OSError, json.JSONDecodeError):
            raise GraphStorage.GraphStorageException(f"Failed to load file {name}_info.json")

    async def get_storage_messages(self, name: str) -> list[dict]:
        try:
            async with aiofiles.open(self._graph_storage_dir / f"{name}_messages.json") as f:
                return json.loads(await f.read())
        except (OSError, json.JSONDecodeError):
            raise GraphStorage.GraphStorageException(f"Failed to load file {name}_messages.json")

    def delete_storage_graph(self, name: str):
        (self._graph_storage_dir / f"{name}.json").unlink(missing_ok=True)
        (self._graph_storage_dir / f"{name}_info.json").unlink(missing_ok=True)
        (self._graph_storage_dir / f"{name}_messages.json").unlink(missing_ok=True)
