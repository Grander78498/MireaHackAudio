from pathlib import Path
import os
import logging

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
    def __new__(cls, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(ML_Models, cls).__new__(cls)
        return cls.instance
    
    def __init__(self,
                 device: str = "",
                 model_whisper_name: str | None = None, 
                 model_bert_name: str | None = None):
        
        if not hasattr(self, "model_whisper") or not hasattr(self, "model_bert"):
            load_dotenv(Path().absolute().as_posix() + '/.env')
            cache_dir = os.getenv('HF_HOME') \
                        if os.getenv('HF_HOME') is not None \
                        else Path().home().joinpath('.cache').as_posix()
            
            if model_whisper_name is None or model_bert_name is None:
                raise Exception('Неверно переданы параметры')
            else:
                self.model_whisper = whisper_ts.load_model(model_whisper_name, device=device, download_root=cache_dir)
                self.model_bert = pipeline("zero-shot-classification", model=model_bert_name, device=device, cache_dir=cache_dir)