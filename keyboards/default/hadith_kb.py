
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Muallif 👤"), KeyboardButton(text="Muqaddima 🗒️")],
        [KeyboardButton(text="Tasodifiy 🧾"), KeyboardButton(text="n-hadis 🧾")],
        [KeyboardButton(text="Menyuga qaytish")]
    ], resize_keyboard=True, row_width=2
)
