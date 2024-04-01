import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from core.filters.isgender import IsGender
from aiogram.filters import Command
from core.handlers.basic import get_start
from core.handlers import form
from core.utils.statesform import StepsForm
from core.settings import settings

async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(form.get_form, F.text == "Начать регистрацию")
    dp.message.register(form.get_age, StepsForm.GET_NAME)
    dp.message.register(form.get_gender, StepsForm.GET_AGE, F.text.isdigit())
    dp.message.register(form.get_location, StepsForm.GET_GENDER, IsGender())
    dp.message.register(form.get_musician_activity, StepsForm.GET_LOCATION, F.location)
    dp.message.register(form.get_type_of_person, StepsForm.GET_MUSICIAN)
    dp.message.register(form.get_back_to_list, StepsForm.GET_TYPE_OF_MUSICIAN)
    dp.mess
    dp.message.register(form.get_fav_musician, StepsForm.GET_BACK)
    dp.message.register(form.get_photo, StepsForm.GET_FAV_MUSICIANS)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
