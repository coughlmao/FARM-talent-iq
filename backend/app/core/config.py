from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    ENV_TYPE: str = "development"

    PORT: int = 8000

    CLIENT_URL: str

    MONGO_URI: str

    MONGO_DB_NAME: str

    CLERK_FRONTEND_API: str
    CLERK_SECRET_KEY: str

    STREAM_API_KEY: str
    STREAM_API_SECRET: str

    INNGEST_SIGNING_KEY: str
    INNGEST_EVENT_KEY: str

    @property
    def is_production(self) -> bool:
        return self.ENV_TYPE.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
