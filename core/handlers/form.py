from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.keyboards.reply import reply_keyboard_registration, reply_keyboard_gender, reply_keyboard_location, musician_activity_keyboard, string_keyboard, keyboards_keyboard, wind_instruments_keyboard, vocal_keyboard_keyboard, drum_keyboard, profession_keyboard, work_with_music_keyboard, other_keyboard,is_it_all
from core.utils.statesform import StepsForm

async def get_form(message: Message, state: FSMContext):
    await message.answer(f"Укажите свое имя.",
                         reply_markup=reply_keyboard_registration)
    await state.set_state(StepsForm.GET_NAME)

async def get_age(message: Message, state: FSMContext):
    await message.answer(f"Укажите свой возраст, {message.text}")
    await state.set_state(StepsForm.GET_AGE)

async def get_gender(message: Message, state: FSMContext):
    await message.answer(f"Укажите свой пол",
                         reply_markup=reply_keyboard_gender)
    await state.set_state(StepsForm.GET_GENDER)

async def get_location(message: Message, state: FSMContext):
    await message.answer(f"Отправьте нам геолокацию",
                         reply_markup=reply_keyboard_location)
    await state.set_state(StepsForm.GET_LOCATION)

async def get_musician_activity(message: Message, state: FSMContext):
    await message.answer(f"Выберите вид музыкальной деятельности:",
                         reply_markup=musician_activity_keyboard)
    await state.set_state(StepsForm.GET_MUSICIAN)

async def get_type_of_person(message: Message, state: FSMContext):
    if message.text == "Инструменталисты – Струнные":
        await message.answer(f"Выберите вид из категории: Инструменталисты – Струнные", reply_markup=string_keyboard)
    elif message.text == "Инструменталисты - Клавишные":
        await message.answer(f"Выберите вид из категории: Инструменталисты - Клавишные", reply_markup=keyboards_keyboard)
    elif message.text == "Инструменталисты - Духовые":
        await message.answer(f"Выберите вид из категории: Инструменталисты - Духовые:", reply_markup=wind_instruments_keyboard)
    elif message.text == "Вокал":
        await message.answer(f"Выберите вид из категории: Вокал",reply_markup=vocal_keyboard_keyboard)
    elif message.text == "Инструменталисты - Ударные":
        await message.answer(f"Выберите вид из категории: Инструменталисты - Ударные", reply_markup=drum_keyboard)
    elif message.text == "Профессии в музыкальной индустрии":
        await message.answer(f"Выберите вид из категории: Профессии в музыкальной индустрии:", reply_markup=profession_keyboard)
    elif message.text == "Работа с музыкой":
        await message.answer(f"Выберите вид из категории: Работа с музыкой", reply_markup=work_with_music_keyboard)
    elif message.text == "Другое":
        await message.answer(f"Выберите вид из категории: Другое", reply_markup=other_keyboard)
    await state.set_state(StepsForm.GET_TYPE_OF_MUSICIAN)


async def get_back_to_list(message: Message, state: FSMContext):
    if message.text == "Вернуться к спискам":
        await message.answer(f"Возвращаемся к спискам", reply_markup=musician_activity_keyboard)
    await state.set_state(StepsForm.GET_TYPE_OF_MUSICIAN)
    await state.update_data(StepsForm.GET_TYPE_OF_MUSICIAN)

async def is_it_all(message: Message, state: FSMContext):
    await message.answer(f"На этом все?", reply_markup=is_it_all)
    await state.set_state(StepsForm.IS_IT_ALL)


async def get_fav_musician(message: Message, state: FSMContext):
    await message.answer(f"Напиши сюда своих <b>любимых исполнителей</b>, чтобы показать свои музыкальные вкусы. Соблюдай оригинальный формат названий. Чем больше - тем лучше!")
    await state.set_state(StepsForm.GET_FAV_MUSICIANS)

async def get_photo(message: Message, state: FSMContext, bot: Bot):
    await message.answer(f"Загрузи своё фото!")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')
    await state.set_state(StepsForm.GET_PHOTO)

async def get_video(message: Message, state: FSMContext):
    await message.answer(f"При наличии, пришли видео, раскрывающее твои способности!")
    await state.finish()