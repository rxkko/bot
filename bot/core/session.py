from aiohttp import ClientSession
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from bot.services.api_client import ApiClient
from bot.core.config import Config

@asynccontextmanager
async def get_api_client() -> AsyncGenerator[ApiClient, None]:
    """
    Создает сессию и API клиент, автоматически закрывает сессию при выходе.

    Использование:
        async with get_api_client() as api_client:
            result = await api_client.get_schedule_by_group(...)
    """
    async with ClientSession() as session:
        api_client = ApiClient(session=session, schedule_url=Config.URL)
        yield api_client