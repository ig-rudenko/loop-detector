import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict

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

    def list_storage_files(self) -> list[GraphStorageFileSchema]:
        try:
            files = [
                f for f in self._graph_storage_dir.iterdir()
                if f.is_file() and f.suffix == '.json' and f.name.startswith('loop_') and
                   not (f.name.endswith("_messages.json") or f.name.endswith("_info.json"))
            ]
        except FileNotFoundError:
            raise GraphStorage.GraphStorageException(f'Graph storage directory not found: `{self._graph_storage_dir}`')

        return sorted(
            (
                GraphStorageFileSchema(name=f.name, modTime=datetime.fromtimestamp(f.stat().st_mtime))
                for f in files
            ),
            key=lambda f: f.modTime,
            reverse=True,
        )

    def get_storage_file(self, name: str) -> GraphSchema:
        try:
            with (self._graph_storage_dir / f"{name}.json").open() as f:
                return GraphSchema.model_validate_json(f.read())
        except (OSError, json.JSONDecodeError):
            raise GraphStorage.GraphStorageException(f'Failed to load file {name}')

    def get_storage_graph_info(self, name: str) -> GraphInfo:
        try:
            with (self._graph_storage_dir / f"{name}_info.json").open() as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            raise GraphStorage.GraphStorageException(f'Failed to load file {name}_info.json')

    def get_storage_messages(self, name: str) -> list[dict]:
        try:
            with (self._graph_storage_dir / f"{name}_messages.json").open() as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            raise GraphStorage.GraphStorageException(f'Failed to load file {name}_messages.json')
