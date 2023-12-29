from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup


class Hadith(StatesGroup):
    hadith_state = State()
