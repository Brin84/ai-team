from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    bot_token: str
    database_url: str
    webhook_url: str
    admin_ids: list[int] = []


    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()