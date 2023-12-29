import requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.surahs import Surah
from states.start import StartCMD
from keyboards.default.oyah_back import back_kb
from keyboards.default.start_kb import main_kb


@dp.message_handler(Command('search_surah'), state=StartCMD.joined_channels)
@dp.message_handler(Text(equals="Sura izlash"), state=StartCMD.joined_channels)
async def search_surah(message: types.Message, state: FSMContext):
    with open("handlers/users/images/surahs.jpg", 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption="Siz Suralar bo'limidasiz!",
                             reply_markup=back_kb)
    await Surah.surah_num.set()


@dp.message_handler(Text(equals="Menyuga qaytish"), state=Surah.surah_num)
async def get_surah_num(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text="Asosiy menyuga qaytdingiz!",
                           reply_markup=main_kb)
    await state.finish()
    await StartCMD.joined_channels.set()


@dp.message_handler(state=Surah.surah_num)
async def send_surah_cmd(message: types.Message):
    text = message.text.replace(' ', '')
    if text.isdigit() and 0 < int(text) < 115:
        surah = int(text)
        req_surah = requests.get(url=f"https://api.alquran.cloud/v1/surah/{surah}")
        data = req_surah.json()

        bot_link = 'https://t.me/test_132_robot'
        bot_nick = 'Quran By Ayah'
        link = 'https://t.me/R_Yusuf_Bot'
        creator = 'Created By SmartCoder'

        surah_name = None
        num_of_ayahs = None
        if 'data' in data and 'number' in data['data']:
            surah_name = data['data']['englishName']
            num_of_ayahs = data['data']['numberOfAyahs']
        edition = 'ar.alafasy'
        req_audio = f"https://cdn.islamic.network/quran/audio-surah/128/{edition}/{surah}.mp3"
        res_audio = requests.get(req_audio)
        await bot.send_audio(chat_id=message.chat.id,
                             audio=res_audio.content,
                             title=f"Mishary Rashid Alafasy - {surah_name} surasi",
                             caption=f"{int(text)} - sura: {surah_name} surasi\n"
                                     f"{surah_name} surasi {num_of_ayahs} oyatdan iborat\n\n"
                                     f"Hozir tinglash 👉 00:00\n\n"
                                     f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                     f"<a href='{link}'>{creator}</a>",
                             parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"{text} - sura mavjud emas!\n"
                                    f"Sura raqami 1 dan 114 gacha oraliqda bo'lishi kerak!\n\n"
                                    f"Sura izlashda yordam oling 👉 /help")
