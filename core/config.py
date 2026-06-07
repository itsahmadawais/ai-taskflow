import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    # Auth
    SERVICE_TOKEN: str

    # LLM
    OPENAI_API_KEY: str

    # Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379

    # DB
    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    # S3
    S3_STORAGE_ENABLED: bool = False
    AWS_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""


def load_settings() -> Settings:
    service_token = os.getenv("SERVICE_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not service_token:
        raise ValueError("SERVICE_TOKEN is not set in .env")

    if not openai_key:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    return Settings(
        SERVICE_TOKEN=service_token,
        OPENAI_API_KEY=openai_key,

        REDIS_HOST=os.getenv("REDIS_HOST", "127.0.0.1"),
        REDIS_PORT=int(os.getenv("REDIS_PORT", "6379")),

        DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3"),

        S3_STORAGE_ENABLED=os.getenv("S3_STORAGE_ENABLED", "false").lower() == "true",

        AWS_BUCKET_NAME=os.getenv("AWS_BUCKET_NAME", ""),
        AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID", ""),
        AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        AWS_REGION=os.getenv("AWS_REGION", ""),
    )


settings = load_settings()