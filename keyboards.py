from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

author_btn = KeyboardButton(text="Муаллиф 👤")
muqaddima_btn = KeyboardButton(text="Муқаддима 🗒️")
rand_hadith = KeyboardButton(text="Тасодифий ҳадис 🧾")
n_hadith = KeyboardButton(text="n-чи ҳадис 🧾")
info_btn = KeyboardButton(text="Бот статистикаси 📊")

main_menu.add(author_btn, muqaddima_btn).add(rand_hadith).add(n_hadith, info_btn)

