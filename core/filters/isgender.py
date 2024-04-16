from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsGender(BaseFilter):
    async def __call__(self, message: Message):
        if message.text == "М" or message.text == "Ж":
            return True
        else:
            await message.answer("Нажми на кнопку М или Ж")
