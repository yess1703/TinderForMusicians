from aiogram.fsm.state import State, StatesGroup


class FindStatesForm:
    FIND_FRIEND = State()
    GET_AGE = State()
    GET_GENDER = State()
    GET_LOCATION = State()
