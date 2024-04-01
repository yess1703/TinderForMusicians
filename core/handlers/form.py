from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.filters.isgender import IsGender
from core.keyboards.reply import (
    drum_keyboard,
    is_it_all_keyboard,
    keyboards_keyboard,
    musician_activity_keyboard,
    other_keyboard,
    profession_keyboard,
    reply_keyboard_gender,
    reply_keyboard_location,
    reply_keyboard_registration,
    string_keyboard,
    vocal_keyboard_keyboard,
    wind_instruments_keyboard,
    work_with_music_keyboard,
)
from core.utils.statesform import StepsForm

router = Router()


@router.message(F.text == "Начать регистрацию")
async def get_form(message: Message, state: FSMContext):
    await message.answer("Укажите свое имя.", reply_markup=reply_keyboard_registration)
    await state.set_state(StepsForm.GET_NAME)


@router.message(StepsForm.GET_NAME)
async def get_age(message: Message, state: FSMContext):
    await message.answer(f"Укажите свой возраст, {message.text}")
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_AGE)


@router.message(StepsForm.GET_AGE, F.text.isdigit())
async def get_gender(message: Message, state: FSMContext):
    await message.answer("Укажите свой пол", reply_markup=reply_keyboard_gender)
    await state.update_data(age=int(message.text))
    await state.set_state(StepsForm.GET_GENDER)


@router.message(StepsForm.GET_GENDER, IsGender())
async def get_location(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте нам геолокацию", reply_markup=reply_keyboard_location
    )
    await state.update_data(gender=message.text)
    await state.set_state(StepsForm.GET_LOCATION)


@router.message(StepsForm.GET_LOCATION, F.location)
async def get_musician_activity(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид музыкальной деятельности:",
        reply_markup=musician_activity_keyboard,
    )
    await state.update_data(location=message.location)
    await state.set_state(StepsForm.GET_MUSICIAN)


@router.message(StepsForm.GET_MUSICIAN)
async def get_type_of_person(message: Message, state: FSMContext):
    if message.text == "Инструменталисты – Струнные":
        await message.answer(
            "Выберите вид из категории: Инструменталисты – Струнные",
            reply_markup=string_keyboard,
        )
    elif message.text == "Инструменталисты – Клавишные":
        await message.answer(
            "Выберите вид из категории: Инструменталисты - Клавишные",
            reply_markup=keyboards_keyboard,
        )
    elif message.text == "Инструменталисты - Духовые":
        await message.answer(
            "Выберите вид из категории: Инструменталисты - Духовые:",
            reply_markup=wind_instruments_keyboard,
        )
    elif message.text == "Вокал":
        await message.answer(
            "Выберите вид из категории: Вокал", reply_markup=vocal_keyboard_keyboard
        )
    elif message.text == "Инструменталисты - Ударные":
        await message.answer(
            "Выберите вид из категории: Инструменталисты - Ударные",
            reply_markup=drum_keyboard,
        )
    elif message.text == "Профессии в музыкальной индустрии":
        await message.answer(
            "Выберите вид из категории: Профессии в музыкальной индустрии:",
            reply_markup=profession_keyboard,
        )
    elif message.text == "Работа с музыкой":
        await message.answer(
            "Выберите вид из категории: Работа с музыкой",
            reply_markup=work_with_music_keyboard,
        )
    elif message.text == "Другое":
        await message.answer(
            "Выберите вид из категории: Другое", reply_markup=other_keyboard
        )
    await state.set_state(StepsForm.GET_TYPE_OF_MUSICIAN)


@router.message(StepsForm.GET_TYPE_OF_MUSICIAN)
async def is_it_all(message: Message, state: FSMContext):
    if message.text == "Вернуться к спискам":
        await message.answer(
            "Возвращаемся к спискам", reply_markup=musician_activity_keyboard
        )
        await state.set_state(StepsForm.GET_MUSICIAN)
    else:
        await message.answer("На этом все?", reply_markup=is_it_all_keyboard)
        data = await state.get_data()
        musicians: set | None = data.get("musicians", None)
        if musicians:
            musicians.add(message.text)
        else:
            musicians = set(message.text)
        await state.update_data(musicians=musicians)
        await state.set_state(StepsForm.IS_IT_ALL)


@router.message(StepsForm.IS_IT_ALL)
async def get_fav_musician(message: Message, state: FSMContext):
    await message.answer(
        "Напиши сюда своих <b>любимых исполнителей</b>, чтобы показать свои музыкальные вкусы. Соблюдай оригинальный формат названий. Чем больше - тем лучше!"
    )
    await state.set_state(StepsForm.GET_FAV_MUSICIANS)


@router.message(StepsForm.GET_FAV_MUSICIANS)
async def get_photo(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Загрузи своё фото!")
    await state.update_data(fav_musicians=message.text)
    await state.set_state(StepsForm.GET_PHOTO)


@router.message(StepsForm.GET_PHOTO, F.photo)
async def get_video(message: Message, state: FSMContext):
    await message.answer("При наличии, пришли видео, раскрывающее твои способности!")
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(StepsForm.GET_VIDEO)


@router.message(StepsForm.GET_VIDEO, F.video)
async def thanks_for_registration(message: Message, state: FSMContext):
    await message.answer("Спасибо за регистрацию! Вот ваш профиль:")
    await state.update_data(video=message.video)
    data = await state.get_data()
    await state.clear()
