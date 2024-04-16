from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from core.database import users_collection
from core.filters.jaccard_similarity import recommend_user
from core.keyboards.dating_inline import (get_likeback_kb,
                                          searching_inline_keyboard)
from core.keyboards.search_reply import lets_go_keyboard
from core.utils.search_states import SearchStepsForm

router = Router()
dp = Dispatcher()


@router.message(SearchStepsForm.GET_STARTED)
async def get_profiles(message: Message, state: FSMContext):
    recommendations = await recommend_user(message.from_user.id)
    if recommendations:
        await message.answer("Создаем Вам рекомендации.", reply_markup=lets_go_keyboard)
        await state.update_data(recommendations=recommendations)
        await state.set_state(SearchStepsForm.REQUEST_PROFILE)
    else:
        await message.answer("Извините, не удалось найти подходящих людей.")


@router.message(SearchStepsForm.REQUEST_PROFILE)
async def show_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    recommendations = data.get("recommendations")
    if recommendations:
        profile, _ = recommendations.pop(0)
        musicians_str = ", ".join(profile["musicians"])
        profile_builder = MediaGroupBuilder(
            caption=
            f"<b>Имя, возраст и город: </b>{profile['name']}, {profile['age']}, {profile['location']}\n"
            f"<b>Описание: </b>{profile["description"]}\n"
            f"<b>Вид музыканта: </b>{musicians_str}\n"
            f"<b>Любимый исполнитель/группа: </b>{profile["fav_musicians"]}"
        )
        if profile["photo"] and profile["video"] == "":
            profile_builder.add_photo(profile["photo"])
            await message.answer_media_group(media=profile_builder.build())
        if profile["photo"] == "" and profile["video"]:
            profile_builder.add_video(profile["video"])
            await message.answer_media_group(media=profile_builder.build())
        if profile["photo"] and profile["video"]:
            profile_builder.add_photo(profile["photo"])
            profile_builder.add_video(profile["video"])
            await message.answer_media_group(media=profile_builder.build())
        if profile["video"] == "" and profile["photo"] == "":
            text = (f"<b>Имя, возраст и город: </b>{profile['name']}, {profile['age']}, {profile['location']}\n"
                    f"<b>Описание: </b>{profile["description"]}\n"
                    f"<b>Вид музыканта: </b>{musicians_str}\n"
                    f"<b>Любимый исполнитель/группа: </b>{profile["fav_musicians"]}")
            await message.answer(text=text)
        await message.answer("Что делать?", reply_markup=searching_inline_keyboard)
        await state.update_data(current_profile_id=profile["_id"])



@router.callback_query(F.data == "next")
async def moving_to_next_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Следующий профиль:")
    data = await state.get_data()
    recommendations = data.get("recommendations")
    if recommendations:
        await state.update_data(recommendations=recommendations)
        await show_profile(callback.message, state)
    else:
        await callback.message.answer("Больше нет рекомендаций")
        await state.clear()


@router.callback_query(F.data == "like")
async def write_to_profile(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    current_profile_id = data.get("current_profile_id")
    user_id = callback.from_user.id
    user_profile = await users_collection.find_one({"_id": user_id})
    if user_profile:
        musicians_str = ", ".join(user_profile['musicians'])
        profile_builder = MediaGroupBuilder(
            caption=
            f"<b>Имя, возраст и город: </b>{user_profile['name']}, {user_profile['age']}, {user_profile['location']}\n"
            f"<b>Описание: </b>{user_profile['description']}\n"
            f"<b>Вид музыканта: </b>{musicians_str}\n"
            f"<b>Любимый исполнитель/группа: </b>{user_profile['fav_musicians']}"
        )
        if user_profile["photo"] and user_profile["video"] == "":
            profile_builder.add_photo(user_profile["photo"])
            await bot.send_media_group(chat_id=str(current_profile_id), media=profile_builder.build())
        if user_profile["photo"] == "" and user_profile["video"]:
            profile_builder.add_video(user_profile["video"])
            await bot.send_media_group(chat_id=str(current_profile_id), media=profile_builder.build())
        if user_profile["photo"] and user_profile["video"]:
            profile_builder.add_photo(user_profile["photo"])
            profile_builder.add_video(user_profile["video"])
            await bot.send_media_group(chat_id=str(current_profile_id), media=profile_builder.build())
        if user_profile["video"] == "" and user_profile["photo"] == "":
            text = (f"<b>Имя, возраст и город: </b>{user_profile['name']}, {user_profile['age']}, {user_profile['location']}\n"
                    f"<b>Описание: </b>{user_profile['description']}\n"
                    f"<b>Вид музыканта: </b>{musicians_str}\n"
                    f"<b>Любимый исполнитель/группа: </b>{user_profile['fav_musicians']}")
            await bot.send_message(chat_id=str(current_profile_id), text=text)

        sender_profile_text = (f"Вашу анкету лайкнул(а): {user_profile['name']}\n"
                               "Вот его/её профиль:")
        await bot.send_message(chat_id=str(current_profile_id), text=sender_profile_text, reply_markup=get_likeback_kb(user_id))
        await state.clear()


@router.callback_query(F.data.startswith("likeback-"))
async def like_back(callback: CallbackQuery, bot: Bot):
    current_profile_id = callback.data.replace("likeback-", "")
    user_id = callback.from_user.id
    await send_matched_user_info(sender_id=user_id, reciever_id=current_profile_id, bot=bot)
    await send_matched_user_info(sender_id=current_profile_id, reciever_id=user_id, bot=bot)


async def send_matched_user_info(sender_id, reciever_id, bot: Bot):
    user_profile = await users_collection.find_one({"_id": int(sender_id)})
    if user_profile:
        sender_username = user_profile.get("username", "Нет информации")
        sender_profile_text = (
            f"Вас лайкнул пользователь: {user_profile['name']}\n"
            f"Username пользователя: @{sender_username}\n"
            "Приятного общения!"
        )
        musicians_str = ", ".join(user_profile['musicians'])
        profile_builder = MediaGroupBuilder(
            caption=
            f"<b>Имя, возраст и город: </b>{user_profile['name']}, {user_profile['age']}, {user_profile['location']}\n"
            f"<b>Описание: </b>{user_profile['description']}\n"
            f"<b>Вид музыканта: </b>{musicians_str}\n"
            f"<b>Любимый исполнитель/группа: </b>{user_profile['fav_musicians']}"
        )
        if user_profile["photo"] and user_profile["video"] == "":
            profile_builder.add_photo(user_profile["photo"])
            await bot.send_media_group(chat_id=reciever_id, media=profile_builder.build())
        if user_profile["photo"] == "" and user_profile["video"]:
            profile_builder.add_video(user_profile["video"])
            await bot.send_media_group(chat_id=reciever_id, media=profile_builder.build())
        if user_profile["photo"] and user_profile["video"]:
            profile_builder.add_photo(user_profile["photo"])
            profile_builder.add_video(user_profile["video"])
            await bot.send_media_group(chat_id=reciever_id, media=profile_builder.build())
        if user_profile["video"] == "" and user_profile["photo"] == "":
            text = (f"<b>Имя, возраст и город: </b>{user_profile['name']}, {user_profile['age']}, {user_profile['location']}\n"
                    f"<b>Описание: </b>{user_profile['description']}\n"
                    f"<b>Вид музыканта: </b>{musicians_str}\n"
                    f"<b>Любимый исполнитель/группа: </b>{user_profile['fav_musicians']}")
            await bot.send_message(chat_id=reciever_id, text=text)
        await bot.send_message(chat_id=reciever_id, text=sender_profile_text)