from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ferretería Conversational AI"
    app_version: str = "1.0.0"
    app_env: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "sqlite+aiosqlite:///./ferreteria_conversational.db"
    auto_create_tables: bool = True
    seed_demo_data: bool = True

    ai_provider: Literal["demo", "openai"] = "demo"
    openai_api_key: SecretStr | None = None
    openai_text_model: str = "gpt-5.6-sol"
    openai_timeout_seconds: float = Field(default=30.0, gt=0, le=300)
    openai_max_retries: int = Field(default=2, ge=0, le=6)
    max_agent_turns: int = Field(default=4, ge=1, le=10)

    realtime_enabled: bool = False
    openai_realtime_model: str = "gpt-realtime-2.1"
    openai_realtime_voice: str = "marin"

    admin_api_key: SecretStr = SecretStr("development-admin-key-change-me")
    cors_origins: list[str] = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:4200",
    ]
    log_level: str = "INFO"
    input_max_characters: int = Field(default=2_000, ge=100, le=20_000)
    chat_history_messages: int = Field(default=14, ge=2, le=50)
    rag_top_k: int = Field(default=4, ge=1, le=10)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_openai_configuration(self) -> "Settings":
        needs_openai = self.ai_provider == "openai" or self.realtime_enabled
        if needs_openai and (
            self.openai_api_key is None or not self.openai_api_key.get_secret_value().strip()
        ):
            raise ValueError(
                "OPENAI_API_KEY is required when AI_PROVIDER=openai or REALTIME_ENABLED=true"
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
