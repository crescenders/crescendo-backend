FROM python:3.11-slim

LABEL authors="goddessana"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libaio1 \
    build-essential && \
    pip install -U pip poetry

WORKDIR /app

COPY . /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --no-dev
