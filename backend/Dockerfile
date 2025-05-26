FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app
COPY ./.env /app

RUN apt-get update && apt-get upgrade && apt-get install -y wget

RUN mkdir -p ~/.opensearch && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
     --output-document ~/.opensearch/root.crt && \
    chmod 0600 ~/.opensearch/root.crt
RUN mkdir -p ~/.mongodb && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
     --output-document ~/.mongodb/root.crt && \
    chmod 0644 ~/.mongodb/root.crt


WORKDIR /app
RUN uv sync --locked