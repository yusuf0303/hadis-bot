from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


regions = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Toshkent"), KeyboardButton(text="Samarqand")],
        [KeyboardButton(text="Andijon"), KeyboardButton(text="Buxoro"), KeyboardButton(text="Farg'ona")],
        [KeyboardButton(text="Guliston"), KeyboardButton(text="Jizzax"), KeyboardButton(text="Qarshi")],
        [KeyboardButton(text="Namangan"), KeyboardButton(text="Navoiy"), KeyboardButton(text="Xiva")],
        [KeyboardButton(text="Nukus ( Qoraqalpog'iston Res )")],
        [KeyboardButton(text="Menyuga qaytish 🔝")]
    ],
    resize_keyboard=True
)

back_region = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Bomdod 🌅"), KeyboardButton(text="Peshin 🕑")],
        [KeyboardButton(text="Asr 🌇"), KeyboardButton(text="Shom 🌆"), KeyboardButton(text="Xufton 🌃")],
        [KeyboardButton(text="Bugun ( To'liq ) 📅"), KeyboardButton(text="Shu hafta ( To'liq ) 🗓️")],
        [KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="Menyuga qaytish 🔝")]
    ],
    resize_keyboard=True
)
