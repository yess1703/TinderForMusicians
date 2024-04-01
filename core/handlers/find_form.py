from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.filters.isgender import IsGender
from core.keyboards.find_reply import gender_keyboard, get_age_of_friend, city_keyboard
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
        "Укажите вид(ы) музыкальной деятельности/владение инструментом(ми)/сферу(ы) деятельности"
    )
