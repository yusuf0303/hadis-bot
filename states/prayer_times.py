from aiogram.dispatcher.filters.state import State, StatesGroup


class PrayerTime(StatesGroup):
    region = State()
    prayer_time_lim = State()
