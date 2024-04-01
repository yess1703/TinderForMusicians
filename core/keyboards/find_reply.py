from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

get_age_of_friend = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Не важно")],
        [KeyboardButton(text="16-20")],
        [KeyboardButton(text="21-25")],
        [KeyboardButton(text="26-30")],
        [KeyboardButton(text="от 31")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="М"), KeyboardButton(text="Ж")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


city_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Не важно")],
        [KeyboardButton(text="СПБ")],
        [KeyboardButton(text="Москва")],
        [KeyboardButton(text="Самара")],
        [KeyboardButton(text="Екатеринбург")],
        [KeyboardButton(text="Казань")],
        [KeyboardButton(text="Рязань")],
        [KeyboardButton(text="Сочи")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

doesnt_matter_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Не важно")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
