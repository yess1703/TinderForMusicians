from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.filters.isgender import IsGender
from core.keyboards.find_reply import (
    adding_keyboard,
    city_keyboard,
    gender_keyboard,
    get_age_of_friend,
)
from core.keyboards.reg_reply import (
    drum_keyboard,
    keyboards_keyboard,
    musician_activity_keyboard,
    other_keyboard,
    profession_keyboard,
    string_keyboard,
    vocal_keyboard_keyboard,
    wind_instruments_keyboard,
    work_with_music_keyboard,
)
from core.utils.find_states import FindStatesForm

router = Router()


@router.message(FindStatesForm.FIND_FRIEND, F.text == "Давай")
async def request_age_of_friend(message: Message, state: FSMContext):
    await message.answer("Укажи примерный возраст", reply_markup=get_age_of_friend)
    await state.set_state(FindStatesForm.GET_AGE)


@router.message(FindStatesForm.GET_AGE)
async def request_gender(message: Message, state: FSMContext):
    await message.answer("Укажите пол", reply_markup=gender_keyboard)
    await state.update_data(age=message.text)
    await state.set_state(FindStatesForm.GET_GENDER)


@router.message(FindStatesForm.GET_GENDER, IsGender())
async def request_location(message: Message, state: FSMContext):
    await message.answer(
        "Укажите локацию, в которой <b>Вы ищете партнера</b>",
        reply_markup=city_keyboard,
    )
    await state.update_data(gender=message.text)
    await state.set_state(FindStatesForm.GET_LOCATION)


@router.message(FindStatesForm.GET_LOCATION)
async def request_city(message: Message, state: FSMContext):
    await message.answer(
        "Укажите вид(ы) музыкальной деятельности/владение инструментом(ми)/сферу(ы) деятельности",
        reply_markup=musician_activity_keyboard,
    )
    await state.update_data(location=message.location)
    await state.set_state(FindStatesForm.GET_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Инструменталисты – Струнные")
async def get_string_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты – Струнные",
        reply_markup=string_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Инструменталисты – Клавишные")
async def get_keyboard_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты - Клавишные",
        reply_markup=keyboards_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Инструменталисты - Духовые")
async def get_wind_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты - Духовые",
        reply_markup=wind_instruments_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Вокал")
async def get_vocals(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Вокал",
        reply_markup=vocal_keyboard_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Инструменталисты - Ударные")
async def get_drum_instruments(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Инструменталисты - Ударные",
        reply_markup=drum_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(
    FindStatesForm.GET_MUSICIAN, F.text == "Профессии в музыкальной индустрии"
)
async def get_profession(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Профессии в музыкальной индустрии",
        reply_markup=profession_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Работа с музыкой")
async def get_work_with_music(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Работа с музыкой",
        reply_markup=work_with_music_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_MUSICIAN, F.text == "Другое")
async def get_others(message: Message, state: FSMContext):
    await message.answer(
        "Выберите вид из категории: Другое",
        reply_markup=other_keyboard,
    )
    await state.set_state(FindStatesForm.GET_TYPE_OF_MUSICIAN)


@router.message(FindStatesForm.GET_TYPE_OF_MUSICIAN)
async def add_one_more(message: Message, state: FSMContext):
    if message.text == "Вернуться к спискам":
        await message.answer(
            "Возвращаемся к спискам", reply_markup=musician_activity_keyboard
        )
        await state.set_state(FindStatesForm.GET_MUSICIAN)
    else:
        await message.answer("На этом все?", reply_markup=adding_keyboard)
        data = await state.get_data()
        musicians: set | None = data.get("musicians", None)
        if musicians:
            musicians.add(message.text)
        else:
            musicians = set(message.text)
        await state.update_data(find_muscian=musicians)
        await state.set_state(FindStatesForm.STOP_ADDING)


@router.message(FindStatesForm.STOP_ADDING, F.text == "Да")
async def perfect_partner(message: Message, state: FSMContext):
    await message.answer(
        "Отлично! Пожалуйста, напиши, чего бы ты хотел от потенциального партнера!"
    )
    await state.set_state(FindStatesForm.GET_PERFECT_PARTNER)


@router.message(FindStatesForm.STOP_ADDING, F.text == "Добавить")
async def add_musicians(message: Message, state: FSMContext):
    await message.answer("Добавьте еще.", reply_markup=musician_activity_keyboard)
    data = await state.get_data()
    musicians2: set | None = data.get("musicians2", None)
    if musicians2:
        musicians2.add(message.text)
    else:
        musicians2 = set(message.text)
    await state.update_data(find_musician2=musicians2)
    await state.set_state(FindStatesForm.GET_MUSICIAN)


@router.message(FindStatesForm.GET_PERFECT_PARTNER)
async def profile_ready(message: Message, state: FSMContext):
    await state.update_data(perfect_partner=message.text)
    await state.clear()
