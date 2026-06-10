from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)


class Settings(BaseSettings):
    database_url: str = Field(default="", validation_alias="DATABASE_URL")
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    llm_provider: str = Field(default="gemini", validation_alias="LLM_PROVIDER")
    secret_key: str = Field(default="", validation_alias="SECRET_KEY")
    app_env: str = Field(default="development", validation_alias="APP_ENV")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
