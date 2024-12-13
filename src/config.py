from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    INTERNAL_ALLOWED_LIST: List[str] = ["127.0.0.1"]
    PROTECTED_PATHS: List[str] = ["/_ui"]
    STORAGE_SECRET: str = "pick-your-private-secret-here"


settings = Settings()
