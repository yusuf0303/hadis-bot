from aiogram import types

from loader import dp, bot

from states.start import StartCMD
from states.sajda_ayahs import SajdaAyah

from keyboards.default.start_kb import main_kb

from keyboards.inline.subscription import check_btn
from data.config import CHANNELS
import utils.misc.subscription


@dp.message_handler(state=StartCMD.startcmd)
async def join_cmd(message: types.Message):
    result = str()
    for channel in CHANNELS:
        status = await utils.misc.subscription.check(user_id=message.from_user.id,
                                                     channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"<b>{channel.title.upper()}</b>ga obuna bo'lgansiz ✅\n"
        else:
            invite_link = await bot.export_chat_invite_link(chat_id=channel.id)
            result += (f"👉 <b>{channel.title.upper()}</b>ga obuna bo'lmagansiz ❌"
                       f"<a href='{invite_link}'>\n👉 Obuna bo'ling 👈</a>\n\n")
    await bot.send_message(chat_id=message.chat.id,
                           text=f"{result}\n\nTekshirish ✔️ tugamisni bosing",
                           parse_mode="HTML",
                           reply_markup=check_btn)


# Echo bot
@dp.message_handler(state=StartCMD.joined_channels)
async def bot_echo(message: types.Message):
    await message.answer("Iltimos quyidagi bo'limlardan birini tanlang 👇👇👇",
                         reply_markup=main_kb)


@dp.message_handler(state=SajdaAyah.sajda_ayah_num)
async def any_from_this(message: types.Message):
    await message.answer("Sajda oyatlari ro'yxatini olish uchun \n"
                         "👉 /sajda_oyatlari 👈 komandasini yuboring!\n"
                         "Asosiy menyuga o'tish uchun pastdagi tugmani bosing 👇")