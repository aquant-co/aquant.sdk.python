FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.5

RUN apt-get update && apt-get install -y \
    curl git unzip vim build-essential \
    libpq-dev gcc && \
    pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION" && \
    apt-get clean

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
