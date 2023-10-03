FROM python:3.11-slim as base

## Environment
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    ## Pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

## Install CURL for healthcheck
RUN apt-get update \
    && apt-get install -y curl

FROM base as build

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM build as run

WORKDIR /app
# EXPOSE 8000

COPY ./src .
