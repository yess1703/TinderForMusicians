from aiogram import Bot
from aiogram.types import Message
async def get_fake_gender(message: Message, bot: Bot):
    await message.answer(f"Нажми на кнопку М или Ж")
