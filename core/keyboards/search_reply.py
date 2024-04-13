from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

search_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Приступим")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

lets_go_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Готов увидеть")]],
    resize_keyboard=True,
    one_time_keyboard=True
)
