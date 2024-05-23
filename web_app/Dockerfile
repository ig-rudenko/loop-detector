FROM python:3.12.3-alpine
LABEL authors="irudenko"

WORKDIR /app

RUN pip install --upgrade --no-cache-dir pip && pip install poetry --no-cache-dir;

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi --no-cache;

COPY . .

ENTRYPOINT ["python"]

CMD ["run.py"]