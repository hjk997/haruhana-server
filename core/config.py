# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE: str = "app.log"
    MONGO_URL: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    BUCKET_NAME: str

    class Config:
        env_file = ".env"   # .env에서 읽기

settings = Settings()