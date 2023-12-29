from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=
    [
        [KeyboardButton(text="Hadis izlash")],
        [KeyboardButton(text="Sura izlash"), KeyboardButton(text="Oyat izlash")],
        [KeyboardButton(text="Sajda oyatlari"), KeyboardButton(text="Namoz vaqtlari")]
    ],
    resize_keyboard=True
)
