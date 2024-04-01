from aiogram import Bot
from aiogram.types import Message

from core.keyboards.reg_reply import reply_keyboard_registration


async def get_start(message: Message, bot: Bot):
    await message.answer(
        f"Приветствую, {message.from_user.first_name}.",
        reply_markup=reply_keyboard_registration,
    )
