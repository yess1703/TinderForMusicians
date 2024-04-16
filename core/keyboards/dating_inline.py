from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

searching_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Лайкнуть", callback_data="like")],
        [InlineKeyboardButton(text="Далее", callback_data="next")],
    ]
)

like_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Лайкнуть", callback_data="likeback")],
        [InlineKeyboardButton(text="Далее", callback_data="next")],
    ]
)


def get_likeback_kb(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Лайкнуть", callback_data=f"likeback-{user_id}"
                )
            ],
            [InlineKeyboardButton(text="Далее", callback_data="next")],
        ]
    )
