FROM python:3.12.6-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --upgrade --no-cache-dir pip;

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-cache;


FROM python:3.12.6-alpine
LABEL authors="irudenko"

ENV PYTHONUNBUFFERED=1

RUN addgroup -g 10001 appgroup \
    && adduser -D -h /app -u 10002 app appgroup \
    && chown -R app:app /app;

# Копируем зависимости из builder-этапа
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

COPY --chown=app:appgroup . .

EXPOSE 8000

CMD ["python", "run.py"]