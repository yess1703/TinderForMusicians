from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (BotCommand, BotCommandScopeDefault, InputMedia,
                           InputMediaVideo, Message)
from aiogram.utils.media_group import MediaGroupBuilder

from core.database import partner_collection, users_collection
from core.keyboards.reg_reply import (go_to_find_form_keyboard,
                                      reply_keyboard_registration)
from core.keyboards.search_reply import search_keyboard
from core.utils.find_states import FindStatesForm
from core.utils.search_states import SearchStepsForm


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="my_profile", description="Мой профиль"),
        BotCommand(command="redo_find_form", description="Перезаполнить форму партнера"),
        BotCommand(command="find_form", description="Лучший партнер"),
        BotCommand(command="search", description="Поиск анкет"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

def show_perfect_partner(age_group, gender, location, musicians, description):
    musicians_str = " ".join(musicians)

    return f"<b>Возраст: </b>{age_group}\n<b>Пол: </b>{gender}\n<b>Город: </b>{location}\n<b>Вид музыканта: </b>{musicians_str}\n<b>Описание: </b>{description}"


async def get_start(message: Message, bot: Bot):
    await message.answer(
        f"Приветствую, {message.from_user.first_name}.",
        reply_markup=reply_keyboard_registration,
    )


async def send_profile_from_db(message: Message):
    user_id = message.from_user.id
    user_profile = await users_collection.find_one({"_id": user_id})
    if user_profile:
        musicians_str = ", ".join(user_profile['musicians'])
        profile_builder = MediaGroupBuilder(
            caption=
            f"<b>Имя и возраст: </b>{user_profile["name"]}, {user_profile["age"]}\n"
            f"<b>Описание: </b>{user_profile["description"]}\n"
            f"<b>Вид музыканта: </b>{musicians_str}\n"
            f"<b>Любимый исполнитель/группа: </b>{user_profile["fav_musicians"]}"
        )
        profile_builder.add_photo(user_profile["photo"])
        if user_profile["video"] != "":
            profile_builder.add_video(user_profile["video"])
        await message.answer_media_group(media=profile_builder.build())
    else:
        await message.answer("Профиль не найден.")


async def redo_find_form(message: Message, state: FSMContext):
    await message.answer("Давайте заполним форму о лучшем подходящем собеседнике заново.", reply_markup=go_to_find_form_keyboard)
    await state.set_state(FindStatesForm.FIND_FRIEND)


async def find_form_profile(message: Message):
    user_id = message.from_user.id
    partner_profile = await partner_collection.find_one({"_id": user_id})
    if partner_profile:
        musicians_str = ", ".join(partner_profile['musicians'])
        if partner_profile["age_group"] == {"$regex": ".*"}:
            partner_profile["age_group"] = "Не важно"
        if partner_profile["gender"] == {"$regex": ".*"}:
            partner_profile["gender"] = "Не важно"
        if partner_profile["location"] == {"$regex": ".*"}:
            partner_profile["location"] = "Не важно"
        text = (
            f"<b>Возраст: </b>{partner_profile["age_group"]}\n"
            f"<b>Пол: </b>{partner_profile["gender"]}\n"
            f"<b>Город: </b>{partner_profile["location"]}\n"
            f"<b>Вид музыканта: </b>{musicians_str}\n"
            f"<b>Описание: </b>{partner_profile["description"]}\n"
        )
        await message.answer(text=text)
    else:
        await message.answer("Вы еще не заполнили анкетирование.")


async def search(message: Message, state: FSMContext):
    await message.answer("Давай приступим к поиску анкет", reply_markup=search_keyboard)
    await state.set_state(SearchStepsForm.GET_STARTED)
