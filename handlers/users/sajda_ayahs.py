import math

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram import types
import requests

from loader import dp, bot
from states.sajda_ayahs import SajdaAyah
from states.start import StartCMD
from keyboards.default.start_kb import main_kb
from keyboards.default.oyah_back import back_kb


@dp.message_handler(Command('sajda_ayahs'), state=StartCMD.joined_channels)
@dp.message_handler(Text(equals="Sajda oyatlari"), state=StartCMD.joined_channels)
async def get_sajda_ayah(message: types.Message, state: FSMContext):
    await message.answer("Siz Sajda Oyatlari bo'limidasiz!\n"
                         "Sajda Oyatlari ro'yxatini olish uchun \n"
                         "👉 /sajda_oyatlari 👈 komandasini yuboring\n"
                         "Asosiy menyuga qaytish uchun pastdagi tugmani bosing 👇",
                         reply_markup=back_kb)
    await SajdaAyah.sajda_ayah_num.set()


@dp.message_handler(Text(equals="Menyuga qaytish"), state=SajdaAyah.sajda_ayah_num)
async def send_sajda_ayahs(message: types.Message, state: FSMContext):
    await message.answer("Asosiy menyuga qaytdingiz!",
                         reply_markup=main_kb)
    await state.finish()
    await StartCMD.joined_channels.set()


@dp.message_handler(Text(equals="/sajda_oyatlari"), state=SajdaAyah.sajda_ayah_num)
async def send_sajda_ayahs(message: types.Message, state: FSMContext):
    global full_caption, bot_link, bot_nick, link, creator
    req = requests.get(url="https://api.alquran.cloud/v1/sajda/quran-uthmani")
    data = req.json()
    ayahs = data['data']['ayahs']
    english_name_lengths = [ayah['surah']['englishName'] for ayah in ayahs]

    max_names_per_caption = 15
    num_captions = math.ceil(len(english_name_lengths) / max_names_per_caption)

    for i in range(num_captions):
        start_index = i * max_names_per_caption
        end_index = (i + 1) * max_names_per_caption
        chunk = english_name_lengths[start_index:end_index]

        full_caption = ''
        for name in chunk:
            number_surah = ayahs[start_index]['surah']['number']
            num_of_ayahs = ayahs[start_index]['surah']['numberOfAyahs']
            num_of_quran = ayahs[start_index]['number']
            num_of_surah = ayahs[start_index]['numberInSurah']
            juz_surah = ayahs[start_index]['juz']
            page_surah = ayahs[start_index]['page']

            full_caption += (f"<b>👇👇 {start_index + 1} - Sajda oyati 👇👇</b>\n\n"
                             f"Sura nomi 👉 <b>{name}</b>\n"
                             f"Qurondagi <b>{number_surah}</b> - sura\n"
                             f"Sura <b>{num_of_ayahs}</b> oyatdan iborat\n"
                             f"Suradagi <b>{num_of_surah}</b> - oyat sajda oyati\n"
                             f"Qurondagi <b>{num_of_quran}</b> - oyat sajda oyati\n"
                             f"<b>{name} surasi {juz_surah} - Juzdan</b> o'rin olgan\n"
                             f"Kitobning <b>{page_surah} - sahifasida</b> kelgan\n\n\n")
            start_index += 1

            creator = "Created by SmartCoder 🧑‍💻"
            link = "https://t.me/R_Yusuf_Bot"
            bot_nick = "Quran By Ayah Bot 🤖"
            bot_link = "https://t.me/test_132_robot"

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{full_caption}\n\n<a href='{bot_link}'>{bot_nick}</a>\n"
             f"<a href='{link}'>{creator}</a>",
        parse_mode=types.ParseMode.HTML
    )
