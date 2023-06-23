FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . /app/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "--log-level", "warning"]
