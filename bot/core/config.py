from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    URL: str
    BOT_TOKEN: str


    class Config:
        env_file = Path(__file__).parent.parent / ".env"
