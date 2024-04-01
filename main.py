import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command

from core.filters.isgender import IsGender
from core.handlers import form
from core.handlers.basic import get_start
from core.handlers.form import router
from core.settings import settings
from core.utils.statesform import StepsForm


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=["start"]))
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
