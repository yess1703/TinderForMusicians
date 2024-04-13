from aiogram import Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from core.database import users_collection
from core.filters.jaccard_similarity import recommend_user
from core.keyboards.dating_inline import searching_inline_keyboard
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
            f"<b>Имя и возраст: </b>{profile["name"]}, {profile["age"]}\n"
            f"<b>Описание: </b>{profile["description"]}\n"
            f"<b>Вид музыканта: </b>{musicians_str}\n"
            f"<b>Любимый исполнитель/группа: </b>{profile["fav_musicians"]}"
        )
        if profile["photo"]:
            profile_builder.add_photo(profile["photo"])
            await message.answer_media_group(media=profile_builder.build())
        if profile["video"]:
            profile_builder.add_video(profile["video"])
            await message.answer_media_group(media=profile_builder.build())
        else:
            text = (f"<b>Имя и возраст: </b>{profile["name"]}, {profile["age"]}\n"
                    f"<b>Описание: </b>{profile["description"]}\n"
                    f"<b>Вид музыканта: </b>{musicians_str}\n"
                    f"<b>Любимый исполнитель/группа: </b>{profile["fav_musicians"]}")
            await message.answer(text=text)
        await message.answer("Что делать?", reply_markup=searching_inline_keyboard)
        await state.update_data(current_profile_id=profile["_id"])


@router.callback_query(F.data == "next")
async def moving_to_next_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Следующий профиль:")
    data = await state.get_data()
    recommendations = data.get("recommendations")
    if recommendations:
        await state.update_data(recommendations=recommendations)
        await show_profile(callback.message, state)
    else:
        await callback.answer("Больше нет рекомендаций")
        await state.clear()


@router.callback_query(F.data == "write")
async def write_to_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_profile_id = data.get("current_profile_id")
    if current_profile_id:
        user_profile = await users_collection.find_one({"_id": current_profile_id})
        if user_profile:
            username = user_profile.get("username")
            if username:
                await callback.message.answer(f"Username пользователя: @{username}")
                return
        await callback.answer("Username пользователя не найден")
    else:
        await callback.answer("ID профиля не найден")
