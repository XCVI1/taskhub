from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_PORT: int = 8000
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    TASKS_SERVICE_URL: str = "http://tasks-service:8002"
    NOTIFICATIONS_SERVICE_URL: str = "http://notifications-service:8003"

settings = Settings()
