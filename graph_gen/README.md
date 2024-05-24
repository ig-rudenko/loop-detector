### Приложение для генерации графа петли на сети

Периодически читает логи сетевого оборудования из `ElasticSearch` и находит 
в поле `message` совпадение строк "loop detected", "detect loop" или "loop guard".

Затем на основе полученных сообщений и IP-адреса оборудования строится граф. 
С помощью приложения `Ecstasy` определяются интерфейсы оборудования, 
которое отправило сообщение о петле, и находится порт, на котором была обнаружена петля.

Данные графа добавляются в кэш `Redis` по ключу `currentLoop:depth=1`,
Глубина графа может быть 1, 2 и 3.

Переменные окружения (и значения по умолчанию):

    log_level = "INFO"
    loop_period = "2m"

    # ECSTASY
    ecstasy_url
    ecstasy_username
    ecstasy_password

    # ElasticSearch
    es_host
    es_port: int = 9200
    es_index
    es_token

    # Redis
    redis_host = ""
    redis_port = 6379
    redis_db = 0
    redis_password = ""

