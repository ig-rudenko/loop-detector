FROM python:3.12.3-alpine
LABEL authors="irudenko"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install --upgrade pip --no-cache-dir &&  \
    pip install poetry --no-cache-dir &&  \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi;

COPY . /app

CMD ["python", "main.py"]
