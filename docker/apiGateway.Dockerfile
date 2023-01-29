FROM python:3.10-slim

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2

WORKDIR /app

RUN pip install "poetry==${POETRY_VERSION}"

COPY src/apiGateway/pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction

COPY src/apiGateway .
