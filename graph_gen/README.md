### Приложение для генерации графа петли на сети

![schema-GraphGen.svg](docs/schema-GraphGen.svg)

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
    STORAGE = "./storage"
    NOTIFICATIONS_CONFIG = "./notifications.json"
    RECORDS_COUNT_NOTIFICATION_LIMIT=0

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

### Объяснение переменных окружения

`LOG_LEVEL` (default "INFO") - уровень логирования ("DEBUG", "INFO", "ERROR")

`LOOP_PERIOD` (default "2m") - период опроса логов. Если указано `2m`, 
то каждые 2 минуты будет опрашиваться elasticsearch в поисках новых логов
за последние 2 минуты. Необходимо указывать в формате 30s, 2m, 1h.

`STORAGE` (default "./storage") - папка хранения файлов графов петель. 
В неё будут храниться json файлы со структурой графа, сообщениями и метаданными.

`NOTIFICATIONS_CONFIG` (default "./notifications.json") - файл с настройками оповещений.
[Шаблон](https://github.com/ig-rudenko/loop-detector/blob/master/web_app/notifications.json).
Данный файл создается через веб-интерфейс приложения и для данного сервиса достаточно прав только на чтение.

`RECORDS_COUNT_NOTIFICATION_LIMIT` (default 0) - является нижним порогом реагирования на петли.
Если количество сообщений о петлях меньше, то можно проигнорировать и не оповещать об этом.

`ECSTASY_URL` - ссылка на главную страницу приложения Ecstasy.
`ECSTASY_USERNAME`, `ECSTASY_PASSWORD` - учетные данные, которые должны иметь доступ
на просмотр сетевого оборудования указанное в логах из elasticsearch.

`ES_HOST` - IP или домен с протоколом (без порта) до elasticsearch, например: `https://elastic.loc`.

`ES_PORT` (default 9200) - порт подключения к elasticsearch.

`ES_INDEX` - шаблон индекса(ов) для поиска логов, можно использовать `*`, например: `netlogs*`.

`ES_TOKEN` - токен для подключения к elasticsearch, который имеет доступ на просмотр `ES_INDEX`.

`REDIS_HOST` - IP или домен Redis.

`REDIS_PORT` (default 6379) - порт подключения к Redis.

`REDIS_DB` (default 0) - номер базы данных Redis.

`REDIS_PASSWORD` (default '') - пароль для подключения к Redis.
