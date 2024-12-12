from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    INTERNAL_ALLOWED_LIST: List[str] = []
    PROTECTED_PATHS: List[str] = ["/_ui"]


settings = Settings()
