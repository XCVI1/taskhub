from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_PORT: int = 8002
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/tasks_db"
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    NOTIFICATIONS_SERVICE_URL: str = "http://notifications-service:8003"

settings = Settings()
