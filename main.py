import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from core.handlers.commands import get_start
from core.handlers.find_form import router as find_form
from core.handlers.registration_form import router as registration_router
from core.settings import settings


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=["start"]))
    dp.include_router(registration_router)
    dp.include_router(find_form)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
