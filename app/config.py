from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    DB_MASTER_URL:  str
    DB_SLAVE_URL:   str
    REDIS_URL: str
    JWT_SECRET_KEY: str

    model_config=SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings=Settings()

