"""
Centralized config, read once and cached.

Why pydantic-settings instead of os.environ scattered through the codebase:
- Every setting is declared in one place with a type and a default, so a typo
  in an env var name fails loudly (validation error) instead of silently
  returning None deep inside some service.
- get_settings() is wrapped in lru_cache so the .env file is parsed once per
  process, not on every request.
- Nothing here reads a Riot API key yet — that gets added in the session
  where we actually build the Riot client, not before.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "LoL Analytics API"
    environment: str = "development"
    debug: bool = True

    # Postgres
    postgres_user: str = "lol_admin"
    postgres_password: str = "changeme_local_only"
    postgres_db: str = "lol_analytics"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # CORS — the Vite dev server's default port. Widen this deliberately later
    # (e.g. for a deployed frontend origin), don't just set it to "*".
    cors_origins: list[str] = ["http://localhost:5173"]

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
