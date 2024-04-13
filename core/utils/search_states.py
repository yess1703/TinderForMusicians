from aiogram.fsm.state import State, StatesGroup


class SearchStepsForm(StatesGroup):
    GET_STARTED = State()
    REQUEST_PROFILE = State()
    GET_PROFILES = State()
    CALLBACK = State()
