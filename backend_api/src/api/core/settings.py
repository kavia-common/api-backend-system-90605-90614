from functools import lru_cache
from typing import List, Optional
from pydantic import BaseModel, field_validator
import os


class Settings(BaseModel):
    """
    Application settings loaded from environment variables.

    Notes:
        - Do not modify .env from code. The orchestrator sets environment variables.
        - Use a .env.example to document which variables are needed.
    """
    app_name: str = "Ocean Professional API"
    environment: str = "development"
    # CORS origins as a comma-separated list in env
    cors_allow_origins_raw: Optional[str] = os.getenv("CORS_ALLOW_ORIGINS", "*")
    # Database URL: default to SQLite file for scaffolding
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    @property
    def cors_allow_origins(self) -> List[str]:
        if not self.cors_allow_origins_raw or self.cors_allow_origins_raw.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_allow_origins_raw.split(",") if o.strip()]

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v: str):
        # Minimal validation; actual engine setup is in db module.
        if not isinstance(v, str) or "://" not in v:
            raise ValueError("DATABASE_URL must be a valid URL string, e.g., sqlite:///./app.db")
        return v


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance loaded from environment variables."""
    return Settings()
