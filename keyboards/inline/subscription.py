from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_btn = InlineKeyboardMarkup(row_width=1)
check = InlineKeyboardButton(text="Tekshirish ✔️", callback_data='check')
check_btn.add(check)
