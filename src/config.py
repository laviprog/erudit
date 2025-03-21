from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
DB_URL = (f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}"
          f":{settings.DB_PORT}/{settings.DB_NAME}")
