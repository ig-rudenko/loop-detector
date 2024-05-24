### Приложение для генерации графа петли на сети

Периодически читает логи сетевого оборудования из `ElasticSearch` и находит 
в поле `message` совпадение строк "loop detected", "detect loop" или "loop guard".

Затем на основе полученных сообщений и IP-адреса оборудования строится граф. 
С помощью приложения `Ecstasy` определяются интерфейсы оборудования, 
которое отправило сообщение о петле, и находится порт, на котором была обнаружена петля.

Данные графа добавляются в кэш `Redis` по ключу `currentLoop:depth=1`,
Глубина графа может быть 1, 2 и 3.

Переменные окружения (и значения по умолчанию):

    LOG_LEVEL = "INFO"
    LOOP_PERIOD = "2m"

    # ECSTASY
    ECSTASY_URL
    ECSTASY_USERNAME
    ECSTASY_PASSWORD

    # ElasticSearch
    ES_HOST
    ES_PORT = 9200
    ES_INDEX
    ES_TOKEN

    # Redis
    REDIS_HOST = ""
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = ""

Пример файла находится в папке `env/sample.env`.
Для прода нужен файл `env/.env`