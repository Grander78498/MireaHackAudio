from pathlib import Path

import aioboto3
from pymongo import AsyncMongoClient
from opensearchpy import AsyncOpenSearch
from fastapi.security import OAuth2PasswordBearer

from project_settings import Settings


settings = Settings()
session = aioboto3.Session()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')



async def get_s3_client():
    """Получение клиента для обращения к S3."""
    async with session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central-1',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key
    ) as s3:
        yield s3


async def get_mongo_client():
    """Получение клиента для обращения к MongoDB."""
    CACERT = Path.home().joinpath('.mongodb/root.crt').as_posix()
    DB_RS = 'rs01'
    DB_NAME = 'db-audio'
    DB_HOST = settings.fqdn_host
    DB_USER = settings.mongo_user
    DB_PASSWORD = settings.mongo_password

    url = f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?replicaSet={DB_RS}&authSource={DB_NAME}'
    
    async with AsyncMongoClient(
        url,
        tls=True,
        tlsCAFile=CACERT
    ) as client:
        yield client


async def get_opensearch_client():
    CACERT = Path.home().joinpath('.opensearch/root.crt').as_posix()
    USER = settings.search_user
    HOSTS = [settings.search_host]
    PASSWORD = settings.search_password

    async with AsyncOpenSearch(
        HOSTS,
        http_auth=(USER, PASSWORD),
        use_ssl=True,
        verify_certs=True,
        ca_certs=CACERT
    ) as client:
        yield client
            