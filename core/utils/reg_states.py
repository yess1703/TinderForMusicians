from aiogram.fsm.state import State, StatesGroup


class RegStepsForm(StatesGroup):
    GET_NAME = State()
    GET_AGE = State()
    GET_GENDER = State()
    GET_FAKE_GENDER = State()
    GET_LOCATION = State()
    GET_MUSICIAN = State()
    GET_TYPE_OF_MUSICIAN = State()
    GET_TYPE_OF_MUSICIAN2 = State()
    IS_IT_ALL = State()
    GET_BACK = State()
    GET_DESCRIPTION = State()
    GET_FAV_MUSICIANS = State()
    GET_PHOTO = State()
    GET_VIDEO = State()
    GET_PROFILE = State()
