from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
import whisper_timestamped as whisper_ts
from transformers import pipeline


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path().absolute().as_posix() +
                                      '/.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')

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


class ML_Models:
    def __new__(cls, **kwargs):  # type: ignore[no-untyped-def]
        if not hasattr(cls, "instance"):
            cls.instance = super(ML_Models, cls).__new__(cls)
        return cls.instance
    
    def __init__(self,
                 device: str = "",
                 transcription_model_name: str | None = None, 
                 tagging_model_name: str | None = None):
        
        if not hasattr(self, "classifier") or not hasattr(self, "transcription_model"):
            load_dotenv(Path().absolute().as_posix() + '/.env')
            cache_dir = os.getenv('HF_HOME') \
                        if os.getenv('HF_HOME') is not None \
                        else Path().home().joinpath('.cache').as_posix()
            
            match (transcription_model_name, tagging_model_name):
                case (None, None) | (_, None) | (None, _):
                    raise Exception('Неверно переданы параметры')
                case (_, _):
                    self.transcription_model = whisper_ts.load_model(transcription_model_name, device=device, download_root=cache_dir)
                    self.classifier = pipeline("zero-shot-classification", model=tagging_model_name, device=device, cache_dir=cache_dir)