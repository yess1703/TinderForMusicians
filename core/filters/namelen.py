from aiogram.filters import BaseFilter
from aiogram.types import Message


class NameLen(BaseFilter):
    async def __call__(self, message: Message):
        if 2 <= len(message.text) <= 30:
            return True
        else:
            await message.answer("Нажми на кнопку М или Ж")
