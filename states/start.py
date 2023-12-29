from aiogram.dispatcher.filters.state import State, StatesGroup


class StartCMD(StatesGroup):
    startcmd = State()
    joined_channels = State()
