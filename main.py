import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from core.handlers.commands import (
    find_form_profile,
    get_profiles,
    get_start,
    redo_find_form,
    send_profile_from_db,
    set_commands,
)
from core.handlers.dating_form import router as dating_form
from core.handlers.find_form import router as find_form
from core.handlers.registration_form import router as registration_router
from core.settings import settings


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    await set_commands(bot)
    dp.message.register(get_start, Command(commands=["start"]))
    dp.include_router(registration_router)
    dp.message.register(send_profile_from_db, Command(commands=["my_profile"]))
    dp.message.register(find_form_profile, Command(commands=["find_form"]))
    dp.message.register(redo_find_form, Command(commands=["redo_find_form"]))
    dp.include_router(find_form)
    dp.include_router(dating_form)
    dp.message.register(get_profiles, Command(commands=["search"]))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
