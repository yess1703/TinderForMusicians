from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import F, Bot
from core.handlers.gender import get_fake_gender

class IsGender(BaseFilter):
    async def __call__(self, message: Message):
        if message.text == "М" or message.text == "Ж":
            return True
        else:
            return get_fake_gender(message)
