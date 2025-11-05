import json
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # Database
    database_url: str
    database_url_sync: str

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "mistral:7b-instruct-q4_0"

    # Embedding
    embedding_model: str = "intfloat/multilingual-e5-base"

    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://stan.frant.pro",
    ]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return json.loads(v)
        return v

    # Rate Limiting
    rate_limit_per_minute: int = 25
    rate_limit_per_hour: int = 100
    rate_limit_per_day: int = 500

    # Environment
    environment: str = "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
