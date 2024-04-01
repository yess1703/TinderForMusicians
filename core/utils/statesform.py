from aiogram.fsm.state import StatesGroup,State

class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_AGE = State()
    GET_GENDER = State()
    GET_FAKE_GENDER = State()
    GET_LOCATION = State()
    GET_MUSICIAN = State()
    GET_TYPE_OF_MUSICIAN = State()
    IS_IT_ALL = State()
    GET_BACK = State()
    GET_FAV_MUSICIANS = State()
    GET_PHOTO = State()