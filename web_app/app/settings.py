from pathlib import Path

from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    base_dir: Path = Path(__file__).parent.parent
    graph_storage: str = (base_dir / "graph_storage").absolute().as_posix()

    log_level: str = "INFO"
    ecstasy_url: str

    redis_host: str = ""
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""


settings = _Config()
Path(settings.graph_storage).mkdir(parents=True, exist_ok=True)
