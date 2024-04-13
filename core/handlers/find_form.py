from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from core.database import partner_collection, users_collection
from core.filters.isgender import IsGender
from core.keyboards.find_reply import (adding_keyboard, city_keyboard,
                                       gender_keyboard, get_age_of_friend)
from core.keyboards.reg_reply import (drum_keyboard, keyboards_keyboard,
                                      musician_activity_keyboard,
                                      other_keyboard, profession_keyboard,
                                      string_keyboard, vocal_keyboard_keyboard,
                                      wind_instruments_keyboard,
                                      work_with_music_keyboard)
from core.utils.find_states import FindStatesForm

router = Router()


def show_perfect_partner(age_group, gender, location, musicians, description):
    musicians_str = " ".join(musicians)
    if age_group == {"$regex": ".*"}:
        age_group = "Не важно"
    if gender == {"$regex": ".*"}:
        gender = "Не важно"
    if location == {"$regex": ".*"}:
        location = "Не важно"
    return f"<b>Возраст: </b>{age_group}\n<b>Пол: </b>{gender}\n<b>Город: </b>{location}\n<b>Вид музыканта: </b>{musicians_str}\n<b>Описание: </b>{description}"


async def get_partner(user_id: int, data: dict):
    existing_user = await partner_collection.find_one({"_id": user_id})
    partner_data = {
        "age_group": data["age_group"],
        "gender": data["gender"],
        "location": data["location"],
        "musicians": list(data.get("musicians", "")),
        "description": data.get("description", ""),
        "photo": data.get("photo", ""),
        "video": data.get("video", ""),
    }
    if existing_user is None:
        full_user_partner_data = {"_id": user_id}
        full_user_partner_data.update(partner_data)
        await partner_collection.insert_one(full_user_partner_data)
    else:
        await partner_collection.update_one(
            {"_id": user_id},
            {"$set": partner_data},
        )


@router.message(FindStatesForm.FIND_FRIEND, F.text == "Давай")
async def request_age_of_friend(message: Message, state: FSMContext):
    await message.answer("Укажи примерный возраст", reply_markup=get_age_of_friend)
    await state.set_state(FindStatesForm.GET_AGE)


@router.message(FindStatesForm.GET_AGE)
async def request_gender(message: Message, state: FSMContext):
    if message.text == "16-20":
        await state.update_data(age_group="16-20")
    if message.text == "21-25":
        await state.update_data(age_group="21-25")
    if message.text == "26-30":
        await state.update_data(age_group="26-30")
    if message.text == "от 31":
        await state.update_data(age_group="от 31")
    if message.text == "Не важно":
        await state.update_data(age_group={"$regex": ".*"})
    await message.answer("Укажите пол", reply_markup=gender_keyboard)
    await state.set_state(FindStatesForm.GET_GENDER)


@router.message(FindStatesForm.GET_GENDER)
async def request_location(message: Message, state: FSMContext):
    if message.text == "М":
        await state.update_data(gender="М")
    if message.text == "Ж":
        await state.update_data(gender="Ж")
    if message.text == "Не важно":
        await state.update_data(gender={"$regex": ".*"})
    await message.answer(
        "Укажите локацию, в которой <b>Вы ищете партнера</b>",
        reply_markup=city_keyboard,
    )
    await state.set_state(FindStatesForm.GET_LOCATION)


@router.message(FindStatesForm.GET_LOCATION)
async def request_city(message: Message, state: FSMContext):
    if message.text == "СПБ":
        await state.update_data(location="СПБ")
    if message.text == "Москва":
        await state.update_data(location="Москва")
    if message.text == "Самара":
        await state.update_data(location="Самара")
    if message.text == "Екатеринбург":
        await state.update_data(location="Екатеринбург")
    if message.text == "Казань":
        await state.update_data(location="Казань")
    if message.text == "Рязань":
        await state.update_data(location="Рязань")
    if message.text == "Сочи":
        await state.update_data(location="Сочи")
    if message.text == "Не важно":
        await state.update_data(location={"$regex": ".*"})
    await message.answer(
        "Укажите вид(ы) музыкальной деятельности/владение инструментом(ми)/сферу(ы) деятельности",
        reply_markup=musician_activity_keyboard,
    )
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
            musicians = {message.text}
        await state.update_data(musicians=musicians)
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
    await state.set_state(FindStatesForm.GET_MUSICIAN)


@router.message(FindStatesForm.GET_PERFECT_PARTNER)
async def profile_ready(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Твой идеальный партнер:")
    partner_data = await state.get_data()
    await get_partner(message.from_user.id, partner_data)
    text = show_perfect_partner(
        partner_data["age_group"],
        partner_data["gender"],
        partner_data["location"],
        partner_data["musicians"],
        partner_data["description"],
    )
    await message.answer(text=text)
    await state.clear()
