## Loop Detector

![techs](https://skillicons.dev/icons?i=elasticsearch,py,redis,fastapi,vue,vite,ts,docker)

---

Приложение помогает выявлять и визуализировать текущие петли на сети, а также просматривать историю их возникновения.

Приложение обрабатывает логи, поступающие от сетевого оборудования, и определяет наличие петель в реальном
времени. При обнаружении петли, приложение предоставляет графическое отображение связей между устройствами,
что позволяет легко локализовать проблему и определить, на каком оборудовании её искать.

![schema](/docs/notification-schema.svg)

Система состоит из трех приложений:

1. GraphGen - генератор графов [Подробнее](https://github.com/ig-rudenko/loop-detector/tree/master/graph_gen#readme).
2. WebApp - приложение на FastAPI для взаимодействия с графами через API.
3. Frontend - Vue+TS+Vite

## Структура приложения

![schema](/docs/schema.svg)

## Настройка

Для работы приложения необходимо иметь настроенные приложение
[Ecstasy](https://github.com/ig-rudenko/ecstasy) и Elasticsearch.

### GraphGen

Нужно создать файл `.env` в папке `graph_gen/env` с переменными окружения.

Пример файла со значениями по умолчанию находится в
`graph_gen/env/sample.env`. На основе этого файла нужно создать свой.

Скопируем и заполним своими данными:

```shell
cp graph_gen/env/sample.env graph_gen/env/.env;
```

Можно его разместить в другом месте, но тогда придется указать его в `docker-compose.yaml` файле.

[Подробнее про настройку GraphGen](https://github.com/ig-rudenko/loop-detector/tree/master/graph_gen#readme).

Далее нужно скопировать JSON файл с начальными правилами поиска сообщений
о петлях в корень проекта. Для этого скопируем базовый файл (если нужно,
в нём можно настроить свои параметры):

```shell
cp graph_gen/config/sample.es-matches.json es-matches.json;
```

### Web App

Нужно также создать файл для переменных окружения.
Пример файла находится в `web_app/env/sample.env`.

Скопируем и заполним своими данными:

```shell
cp web_app/env/sample.env web_app/env/.env;
```

## Запуск

Перед запуском нужно создать файл в корне проекта (изначально пустой) для хранения настроек
оповещений о новых петлях. По умолчанию в docker-compose.yaml его название
указано как `notifications.json`. Там будут храниться способы оповещений.

Не удаляйте этот файл в дальнейшем!

```shell
touch notifications.json;
```

Приложение запускается с помощью:

```shell
docker compose up -d
```

Приложение будет сохранять граф петель и его сообщения в json файлы.
Хранилище по умолчанию указано как `./loop_storage`.

## Визуализация

![img.png](docs/img/img.png)

![img.png](docs/img/img_1.png)

![img.png](docs/img/img_2.png)

![img.png](docs/img/img_3.png)

