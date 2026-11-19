import asyncio
from bot.handlers.schedule import router
from aiogram import Bot, Dispatcher
from bot.core.config import Config

bot = Bot(token="8229113560:AAGKtYfKdZMXILx_cU7QcIA9Bzq3nSQCLN4")

dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())