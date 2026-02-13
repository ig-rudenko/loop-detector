FROM python:3.13.5-alpine AS builder

RUN apk update && apk add curl

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --upgrade --no-cache-dir pip;

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi --no-cache;


FROM python:3.13.5-alpine
LABEL authors="irudenko"

ENV PYTHONUNBUFFERED=1

RUN addgroup -g 10001 appgroup \
    && adduser -D -h /app -u 10002 app appgroup \
    && chown -R app:app /app;

# Копируем зависимости из builder-этапа
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

COPY --chown=app:appgroup . .

EXPOSE 8000

CMD ["python", "main.py"]