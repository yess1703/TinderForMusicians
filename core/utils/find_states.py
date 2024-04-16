from aiogram.fsm.state import State, StatesGroup


class FindStatesForm(StatesGroup):
    FIND_FRIEND = State()
    GET_AGE = State()
    GET_GENDER = State()
    GET_LOCATION = State()
    GET_MUSICIAN = State()
    GET_TYPE_OF_MUSICIAN = State()
    STOP_ADDING = State()
    GET_PERFECT_PARTNER = State()
