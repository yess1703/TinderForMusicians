from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

reply_keyboard_registration = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Начать регистрацию"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Приступим?",
)

reply_keyboard_gender = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="М"), KeyboardButton(text="Ж")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

reply_keyboard_location = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить геолокацию", request_location=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


musician_activity_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Инструменталисты – Струнные")],
        [KeyboardButton(text="Инструменталисты – Клавишные")],
        [KeyboardButton(text="Инструменталисты - Духовые")],
        [KeyboardButton(text="Инструменталисты - Ударные")],
        [KeyboardButton(text="Вокал")],
        [KeyboardButton(text="Профессии в музыкальной индустрии")],
        [KeyboardButton(text="Работа с музыкой")],
        [KeyboardButton(text="Другое")],
    ],
    one_time_keyboard=True,
    input_field_placeholder="Выберите свою сферу",
)

string_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Гитарист")],
        [KeyboardButton(text="Бас-гитарист")],
        [KeyboardButton(text="Виолончелист")],
        [KeyboardButton(text="Укулеле")],
        [KeyboardButton(text="Скрипач")],
        [KeyboardButton(text="Альтист")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

keyboards_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Клавишник")],
        [KeyboardButton(text="Аккордеонист")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

wind_instruments_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Духовик")],
        [KeyboardButton(text="Кларнетист")],
        [KeyboardButton(text="Флейтист")],
        [KeyboardButton(text="Гобоист")],
        [KeyboardButton(text="Саксофонист")],
        [KeyboardButton(text="Тромбонист")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

vocal_keyboard_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вокалист")],
        [KeyboardButton(text="Бэк-вокалист")],
        [KeyboardButton(text="Рэпер")],
        [KeyboardButton(text="Битбоксер")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

drum_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Барабанщик")],
        [KeyboardButton(text="Кахонист")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

profession_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Композитор")],
        [KeyboardButton(text="Продюсирование")],
        [KeyboardButton(text="Промоутер")],
        [KeyboardButton(text="Звукоинженер")],
        [KeyboardButton(text="Тур-менеджер")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

work_with_music_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Битмейкер")],
        [KeyboardButton(text="DJ")],
        [KeyboardButton(text="Автор текстов")],
        [KeyboardButton(text="Мастеринг и сведение")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

other_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оператор")],
        [KeyboardButton(text="Band-группа")],
        [KeyboardButton(text="Художник")],
        [KeyboardButton(text="Графический редактор")],
        [KeyboardButton(text="Фотограф")],
        [KeyboardButton(text="Вернуться к спискам")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

is_it_all_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да")], [KeyboardButton(text="Добавить")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
