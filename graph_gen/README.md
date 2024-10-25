### Приложение для генерации графа петли на сети

![schema-GraphGen.svg](docs/schema-GraphGen.svg)

Периодически читает логи сетевого оборудования из `ElasticSearch` по правилу,
которое записано в JSON файле (пример в `config/sample.es-matches.json`).
Данный файл добавляется внутрь докер контейнера и указывается в переменных окружения ниже.

Затем на основе полученных сообщений и IP-адреса оборудования строится граф.
С помощью приложения `Ecstasy` определяются интерфейсы оборудования,
которые отправили сообщения о петле.
Также находится порт, на котором была обнаружена петля.

Данные графа добавляются в кэш `Redis` по ключу `currentLoop:depth=1`,
Глубина графа может быть 1, 2 и 3.

Переменные окружения (и значения по умолчанию):

    LOG_LEVEL="INFO"
    LOOP_PERIOD="2m"
    
    # Путь внутри контейнера (относительно папки /app)
    STORAGE="./storage"
    
    RECORDS_COUNT_NOTIFICATION_LIMIT=0
    
    # Путь внутри контейнера (относительно папки /app)
    NOTIFICATIONS_CONFIG="./notifications.json"
    
    CACHE_TIMEOUT=300
    
    # Нужно указывать вместе со схемой (http или https)
    ECSTASY_URL=http://
    ECSTASY_USERNAME
    ECSTASY_PASSWORD
    
    # Нужно указывать вместе со схемой (http или https)
    ES_HOST=http://
    ES_PORT=9200
    ES_INDEX=
    ES_TOKEN=

    ES_JQ_DEVICE_IP=.host.ip
    ES_JQ_MESSAGE=.message
    
    # Название полей в elasticsearch индексе
    ES_FIELD_DEVICE_IP=host
    ES_FIELD_MESSAGE=message

    # Путь внутри контейнера (относительно папки /app)
    ES_MATCHES_FILE="./es-matches.json"
    
    REDIS_HOST=redis
    REDIS_PORT=6379
    REDIS_DB=0
    REDIS_PASSWORD=""

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

В формате DSL JQ,указывают где в вашем случае искать поля IP и сообщения в ответе.
https://jqlang.github.io/jq/tutorial/

[Пример](https://jqplay.org/s/Es7NQKJyPPloIfT) как найти поля.

`ES_JQ_DEVICE_IP` - JSON Query для поиска значения IP адреса в логе.

`ES_JQ_MESSAGE` - JSON Query для поиска значения текста сообщения в логе.

`ES_FIELD_DEVICE_IP` - В каком поле хранится IP адрес.

`ES_FIELD_MESSAGE` - В каком поле хранится сообщение.

`ES_MATCHES_FILE` - JSON файл, в котором содержится правила для поиска в elasticsearch сообщений о петлях

`REDIS_HOST` - IP или домен Redis.

`REDIS_PORT` (default 6379) - порт подключения к Redis.

`REDIS_DB` (default 0) - номер базы данных Redis.

`REDIS_PASSWORD` (default '') - пароль для подключения к Redis.

## Пример настройки GraphGen

Для начала посмотрите в какой индекс у вас пишутся логи оборудования.

Допустим это `devices_logs-YYYY.mm.dd` и каждый день создается новый индекс,
что чаще всего можно встретить.

Тогда переменная `ES_INDEX` будет равна
`devices_logs*`, чтобы учитывать любой день.

Далее смотрим формат записи одного лога. Для этого можно использовать _kibana_
либо запросить через _API_.

```json
{
  "_index": "devices_log-2024.09.19-1",
  "_id": "N15FCZIBU8acjZQaqB23",
  "_score": 15.064758,
  "_source": {
    "@version": "1",
    "@timestamp": "2024-09-19T07:53:33.010265027Z",
    "event": {
      "original": "<188> Sep 19 10:53:32 ELRP.Report: [CLI:v12:42] LOOP DETECTED : 88746402 transmitted, 35 received, ingress slot:port (5) egress slot:port (5)"
    },
    "type": "network-logs",
    "message": "<188> Sep 19 10:53:32 ELRP.Report: [CLI:v12:42] LOOP DETECTED : 88746402 transmitted, 35 received, ingress slot:port (5) egress slot:port (5)",
    "host": {
      "ip": "172.30.0.10"
    }
  }
}
```

Тут обращаем внимание на поля, где хранятся сообщение и IP адрес.

Так как IP адрес находится внутри поля `host`, то указываем только его.
Тогда переменные окружения будут иметь такие значения.

`ES_FIELD_DEVICE_IP=host`

`ES_FIELD_MESSAGE=message`

Переменные для поиска значений:

`ES_JQ_DEVICE_IP=.host.ip`

`ES_JQ_MESSAGE=.message`

Теперь сформируем запрос на поиск фильтрацию логов.
Сформируем в корне проекта `loop-detected` файл, для этого можно скопировать
пример.

```shell
cp graph_gen/config/sample.es-matches.json es-matches.json;
```

Внутри файла нужно указать параметры для поиска только сообщений петель.
Обязательно проверьте что поле `message`, указанное ниже имеется у вас в
формате логов, если нет - то укажите своё.

```json
{
  "should": [
    {
      "match_phrase": {
        "message": "loop detected"
      }
    },
    {
      "match_phrase": {
        "message": "detect loop"
      }
    },
    {
      "match_phrase": {
        "message": "loop guard"
      }
    }
  ]
}
```

Период опроса оставим без изменений:

`LOOP_PERIOD="2m"`

Укажем данные для подключения к [Ecstasy](https://github.com/ig-rudenko/ecstasy)
и Elasticsearch.
