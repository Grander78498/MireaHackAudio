from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    aws_access_key_id: str
    aws_secret_access_key: str
    bucket: str

    fqdn_host: str
    mongo_user: str
    mongo_password: str

    debug: bool