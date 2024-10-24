from pathlib import Path

from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    base_dir: Path = Path(__file__).parent.parent

    storage: str
    notifications_config: str
    es_matches_file: str

    records_count_notification_limit: int = 0

    cache_timeout: int = 300

    log_level: str = "INFO"
    # Loop daemon
    loop_period: str = "2m"

    # ECSTASY
    ecstasy_url: str
    ecstasy_username: str
    ecstasy_password: str

    # ElasticSearch
    es_host: str
    es_port: int = 9200
    es_index: str
    es_token: str

    es_jq_device_ip: str = ".host.ip"
    es_jq_message: str = ".message"

    es_field_device_ip: str = "host"
    es_field_message: str = "message"

    # Redis
    redis_host: str = ""
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    @property
    def storage_path(self):
        return self.base_dir / self.storage

    @property
    def notifications_config_path(self):
        return self.base_dir / self.notifications_config

    @property
    def es_matches_file_path(self):
        return self.base_dir / self.es_matches_file


settings = _Config()
