from aiogram import Bot
from aiogram.types import Message

from core.keyboards.reply import reply_keyboard_gender, reply_keyboard_registration


async def get_start(message: Message, bot: Bot):
    await message.answer(
        f"Приветствую, {message.from_user.first_name}.",
        reply_markup=reply_keyboard_registration,
    )


async def get_name(message: Message, bot: Bot):
    await message.answer(f"Укажите свое имя")


async def get_age(message: Message, bot: Bot):
    await message.answer(f"Укажите возраст")


async def get_gender(message: Message, bot: Bot):
    await message.answer(f"Укажите свой пол", reply_markup=reply_keyboard_gender)


async def get_photo(message: Message, bot: Bot):
    await message.answer(f"Отлично, ты отправил картинку")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, "photo.jpg")
