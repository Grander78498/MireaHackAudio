from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path().absolute().parent.as_posix() + '/.env', env_file_encoding='utf-8')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return dotenv_settings, env_settings

    aws_access_key_id: str
    aws_secret_access_key: str
    bucket: str

    fqdn_host: str
    mongo_user: str
    mongo_password: str

    search_host: str
    dashboard_host: str
    search_user: str
    search_password: str