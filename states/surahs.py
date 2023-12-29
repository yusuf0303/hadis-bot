from aiogram.dispatcher.filters.state import State, StatesGroup


class Surah(StatesGroup):
    surah_num = State()
