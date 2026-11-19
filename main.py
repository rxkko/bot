import asyncio
from bot.handlers.schedule import router
from aiogram import Bot, Dispatcher
from bot.core.config import config

bot = Bot(token=config.BOT_TOKEN)

dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())