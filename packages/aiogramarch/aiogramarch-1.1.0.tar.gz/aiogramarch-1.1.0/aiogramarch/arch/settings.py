""" Сборка переменных окружения из dotenv """

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_URL: str

    AIOGRAM_PROJECT_NAME: str
    AIOGRAM_PROJECT_DIR: str
    AIOGRAM_PROJECT_APPS_DIR: str

    class Config:
        case_sensitive = True
        env_file = "env.env"


settings = Settings()
