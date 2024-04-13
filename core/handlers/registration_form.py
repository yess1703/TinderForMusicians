from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from core.database import users_collection
from core.filters.isgender import IsGender
from core.filters.namelen import NameLen
from core.keyboards.reg_reply import (drum_keyboard, go_to_find_form_keyboard,
                                      is_it_all_keyboard, keyboards_keyboard,
                                      moving_on_keyboard,
                                      musician_activity_keyboard,
                                      other_keyboard, profession_keyboard,
                                      reply_keyboard_gender,
                                      reply_keyboard_location,
                                      reply_keyboard_registration,
                                      string_keyboard, video_keyboard,
                                      vocal_keyboard_keyboard,
                                      wind_instruments_keyboard,
                                      work_with_music_keyboard)
from core.utils.find_states import FindStatesForm
from core.utils.reg_states import RegStepsForm

router = Router()


def show_profile(name, age, description, musicians, fav_musicians):
    musicians_str = " ".join(musicians)
    return f"<b>Имя и возраст: </b>{name}, {age}\n<b>Описание: </b>{description}\n<b>Вид музыканта: </b>{musicians_str}\n<b>Любимый исполнитель/группа: </b>{fav_musicians}"


async def add_user(user_id: int, data: dict):
    existing_user = await users_collection.find_one({"_id": user_id})
    user_data = {
        "username": data["username"],
        "name": data["name"],
        "age": data["age"],
        "age_group": get_age_group(data["age"]),
        "gender": data["gender"],
        "location": data["location"],
        "description": data.get("description", ""),
        "musicians": list(data.get("musicians", "")),
        "fav_musicians": data.get("fav_musicians", ""),
        "photo": data.get("photo", ""),
        "video": data.get("video", ""),
    }
    if existing_user is None:
        full_user_data = {"_id": user_id}
        full_user_data.update(user_data)
        await users_collection.insert_one(full_user_data)
    else:
        await users_collection.update_one(
            {"_id": user_id},
            {"$set": user_data},
        )


def get_age_group(age: int):
    if age < 21:
        return "16-20"
    if age < 26:
        return "21-25"
    if age < 31:
        return "26-30"
    return "от 31"


@router.message(F.text == "Начать регистрацию")
async def get_form(message: Message, state: FSMContext):
    await message.answer("Укажите свое имя.", reply_markup=reply_keyboard_registration)
    await state.set_state(RegStepsForm.GET_NAME)


@router.message(RegStepsForm.GET_NAME, NameLen())
async def request_age(message: Message, state: FSMContext):
    await message.answer(f"Укажите свой возраст, {message.text}")
    await state.update_data(name=message.text)
    await state.update_data(username=message.from_user.username)
    await state.set_state(RegStepsForm.GET_AGE)


@router.message(RegStepsForm.GET_AGE, F.text.isdigit())
async def request_gender(message: Message, state: FSMContext):
    await message.answer("Укажите свой пол", reply_markup=reply_keyboard_gender)
    await state.update_data(age=int(message.text))
    await state.set_state(RegStepsForm.GET_GENDER)


@router.message(RegStepsForm.GET_GENDER, IsGender())
async def request_location(message: Message, state: FSMContext):
    await message.answer(
        "Выберите ваш город из списка", reply_markup=reply_keyboard_location
    )
    await state.update_data(gender=message.text)
    await state.set_state(RegStepsForm.GET_LOCATION)


@router.message(RegStepsForm.GET_LOCATION)
async def request_musician_activity(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид музыкальной деятельности:",
        reply_markup=musician_activity_keyboard,
    )
    await state.update_data(location=message.text)
    await state.set_state(RegStepsForm.GET_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Инструменталисты – Струнные")
async def get_string_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты – Струнные",
        reply_markup=string_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Инструменталисты – Клавишные")
async def get_keyboard_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты - Клавишные",
        reply_markup=keyboards_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Инструменталисты - Духовые")
async def get_wind_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты - Духовые",
        reply_markup=wind_instruments_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Вокал")
async def get_vocals(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Вокал",
        reply_markup=vocal_keyboard_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Инструменталисты - Ударные")
async def get_drum_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты - Ударные",
        reply_markup=drum_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(
    RegStepsForm.GET_MUSICIAN, F.text == "Профессии в музыкальной индустрии"
)
async def get_profession(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Профессии в музыкальной индустрии",
        reply_markup=profession_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Работа с музыкой")
async def get_work_with_music(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Работа с музыкой",
        reply_markup=work_with_music_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_MUSICIAN, F.text == "Другое")
async def get_others(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Другое",
        reply_markup=other_keyboard,
    )
    await state.set_state(RegStepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(RegStepsForm.GET_TYPE_OF_MUSICIAN)
async def add_one_more(message: Message, state: FSMContext):
    if message.text == "Вернуться к спискам":
        await message.answer(
            "Возвращаемся к спискам", reply_markup=musician_activity_keyboard
        )
        await state.set_state(RegStepsForm.GET_MUSICIAN)
    else:
        await message.answer("На этом все?", reply_markup=is_it_all_keyboard)
        data = await state.get_data()
        musicians: set | None = data.get("musicians", None)
        if musicians:
            musicians.add(message.text)
        else:
            musicians = {message.text}
        await state.update_data(musicians=musicians)
        await state.set_state(RegStepsForm.IS_IT_ALL)


@router.message(RegStepsForm.IS_IT_ALL, F.text == "Да")
async def request_description(message: Message, state: FSMContext):
    await message.answer(
        "Отлично! Пожалуйста, расскажи о себе, опиши деятельность подробнее! Учитывай опыт деятельности, более узкое "
        "направление деятельности, жанровые предпочтения, музыкальную базу, музыкальное образование (при наличии). "
        "Чем подробнее ты расскажешь о себе, тем больше вероятность, что тебя заметят!"
    )
    await state.set_state(RegStepsForm.GET_DESCRIPTION)


@router.message(RegStepsForm.IS_IT_ALL, F.text == "Добавить")
async def add_musicians(message: Message, state: FSMContext):
    await message.answer("Добавьте еще.", reply_markup=musician_activity_keyboard)
    await state.set_state(RegStepsForm.GET_MUSICIAN)


@router.message(RegStepsForm.GET_DESCRIPTION)
async def request_fav_musician(message: Message, state: FSMContext):
    await message.answer(
        "Напиши сюда своих <b>любимых исполнителей</b>, чтобы показать свои музыкальные вкусы. Соблюдай оригинальный "
        "формат названий. Чем больше - тем лучше!"
    )
    await state.update_data(description=message.text)
    await state.set_state(RegStepsForm.GET_FAV_MUSICIANS)


@router.message(RegStepsForm.GET_FAV_MUSICIANS)
async def request_photo(message: Message, state: FSMContext):
    await message.answer("Загрузи своё фото!")
    await state.update_data(fav_musicians=message.text)
    await state.set_state(RegStepsForm.GET_PHOTO)


@router.message(RegStepsForm.GET_PHOTO, F.photo)
async def request_video(message: Message, state: FSMContext):
    await message.answer(
        "При наличии, пришли видео, раскрывающее твои способности!",
        reply_markup=video_keyboard,
    )
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(RegStepsForm.GET_VIDEO)


@router.message(RegStepsForm.GET_VIDEO, F.text == "Возможно, позже")
async def maybe_later(message: Message, state: FSMContext):
    await message.answer(
        "Хорошо, ты сможешь добавить видео позже. \n"
        "Спасибо за регистрацию. Вот Ваш профиль.",
        reply_markup=moving_on_keyboard,
    )
    data = await state.get_data()
    await add_user(message.from_user.id, data)
    profile_builder = MediaGroupBuilder(
        caption=show_profile(
            data["name"],
            data["age"],
            data["description"],
            data["musicians"],
            data["fav_musicians"],
        )
    )
    profile_builder.add_photo(data["photo"])
    await message.answer_media_group(media=profile_builder.build())
    await state.set_state(RegStepsForm.GET_PROFILE)


@router.message(RegStepsForm.GET_VIDEO, F.video)
async def thanks_for_registration(message: Message, state: FSMContext):
    await message.answer(
        "Спасибо за регистрацию! Вот Ваш профиль.", reply_markup=moving_on_keyboard
    )
    await state.update_data(video=message.video.file_id)
    data = await state.get_data()
    await add_user(message.from_user.id, data)
    profile_builder = MediaGroupBuilder(
        caption=show_profile(
            data["name"],
            data["age"],
            data["description"],
            data["musicians"],
            data["fav_musicians"],
        )
    )
    profile_builder.add_photo(data["photo"])
    profile_builder.add_video(data["video"])
    await message.answer_media_group(media=profile_builder.build())
    await state.set_state(RegStepsForm.GET_PROFILE)


@router.message(RegStepsForm.GET_PROFILE, F.text == "Двигаемся дальше")
async def move_to_find_form(message: Message, state: FSMContext):
    await message.answer(
        "Твой профиль создан. Теперь приступим к заполнению анкетирования о твоем идеальном партнере.",
        reply_markup=go_to_find_form_keyboard,
    )
    await state.clear()
    await state.set_state(FindStatesForm.FIND_FRIEND)
