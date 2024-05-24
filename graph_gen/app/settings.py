from pydantic_settings import BaseSettings


class _Config(BaseSettings):
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

    # Redis
    redis_host: str = ""
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""


settings = _Config()
