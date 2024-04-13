from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.filters.jaccard_similarity import recommend_user

searching_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать", callback_data="write")],
        [InlineKeyboardButton(text="Далее", callback_data="next")],
    ]
)
