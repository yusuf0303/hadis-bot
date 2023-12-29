from aiogram import types
import requests
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import Command


from keyboards.default.oyah_back import back_kb
from keyboards.default.start_kb import main_kb

from loader import dp, bot
from states.ayahs import Ayah
from states.start import StartCMD


@dp.message_handler(Command('search_ayah'), state=StartCMD.joined_channels)
@dp.message_handler(Text(equals="Oyat izlash"), state=StartCMD.joined_channels)
async def search_ayah(message: types.Message, state: FSMContext):
    await message.answer("Siz oyatlar bo'limidasiz!",
                         reply_markup=back_kb)
    await Ayah.ayah_num.set()


@dp.message_handler(Text(equals="Menyuga qaytish"), state=Ayah.ayah_num)
async def get_ayah_num(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text="Asosiy menyuga qaytdingiz!",
                           reply_markup=main_kb)
    await state.finish()
    await StartCMD.joined_channels.set()


@dp.message_handler(state=Ayah.ayah_num)
async def send_ayah_cmd(message: types.Message):
    sent_msg = await message.answer("Siz Oyatlar bo'limidasiz!")
    parts = message.text.replace(' ', '').split(':')
    if len(parts) == 2 and all(part.isdigit() for part in parts):
        sec = 5
        while sec > 0:
            await asyncio.sleep(1)
            await bot.edit_message_text(message_id=sent_msg.message_id,
                                        chat_id=message.chat.id,
                                        text=f"Ma'lumotlar olinmoqda: {sec} sekund qoldi")
            sec -= 1
        await bot.delete_message(chat_id=message.chat.id, message_id=sent_msg.message_id)
        surah, ayah = message.text.split(':')
        surah = int(surah)
        ayah = int(ayah)
        if surah < 0 or surah > 114:
            await message.answer(text=f"{surah} - Sura mavjud emas!\n"
                                      f"Sura raqami 1 dan 114 gacha bo'lishi kerak!")
        else:
            req_all_ayah = requests.get(url=f"https://api.alquran.cloud/v1/surah/{surah}")
            data = req_all_ayah.json()
            eng_name = data['data']['englishName']
            all_ayahs = data['data']['numberOfAyahs']
            if ayah < 1 or ayah > all_ayahs:
                await message.reply(text=f"<b>{surah} - sura: {eng_name} surasi {all_ayahs} oyatdan iborat.</b>\n"
                                         f"Oyat raqami <b>1</b> dan <b>{all_ayahs}</b> gacha "
                                         f"oraliqda bo'lishi kerak!",
                                    parse_mode="HTML")
            else:
                data_audio = None
                req = requests.get(url=f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}")
                data = req.json()
                if 'data' in data and 'number' in data['data']:
                    data_audio = data['data']['number']
                req_audio = requests.get(url=f"https://cdn.islamic.network/quran/audio/128/ar.alafasy/{data_audio}.mp3")
                if req.status_code == 200 and req_audio.status_code == 200:
                    data = req.json()['data']
                    ayah_total_number = data['number']
                    ayah_text = data['text']
                    surah_num = data['surah']['number']
                    ayah_number = data['numberInSurah']
                    surah_name = data['surah']['englishName']
                    all_ayahs = data['surah']['numberOfAyahs']
                    juz_num = data['juz']
                    page = data['page']
                    sajda = data['sajda']
                    yes = " oyati‼️"
                    no = "oyati emas ‼️"

                    creator = 'Created By SmartCoder'
                    link = "https://t.me/R_Yusuf_Bot"
                    bot_nick = "Surah By Ayah Bot"
                    bot_link = "https://t.me/test_132_robot"

                    req_photo = f"https://cdn.islamic.network/quran/images/high-resolution/{surah}_{ayah}.png"
                    res_photo = requests.get(req_photo)

                    await bot.send_photo(chat_id=message.chat.id,
                                         photo=res_photo.content,
                                         caption=f"Sura nomi 👉 <strong>{surah_name}</strong>\n"
                                                 f"Qurondagi <strong>{surah_num} - sura</strong>\n"
                                                 f"{surah_name} surasi <strong>{juz_num} - Juz</strong>dan o'rin olgan"
                                                 f"\nSura <strong>{all_ayahs}</strong> oyatdan iborat\n"
                                                 f"Ushbu oyat Qurondagi <strong>{ayah_total_number}</strong> - oyat\n"
                                                 f"Ushbu oyat Suradagi <strong>{ayah_number}</strong> - oyat\n"
                                                 f"Kitobning <strong>{page} - sahifasida</strong> kelgan\n"
                                                 f"<strong>⚠️ {surah_name} surasi {ayah_number} - oyat Sajda "
                                                 f"{yes if sajda else no}</strong>\n"
                                                 f"\nOyat matni 👇\n\n<code>{ayah_text}</code>\n\n"
                                                 f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                                 f"<a href='{link}'>{creator}</a>",
                                         parse_mode="HTML")
                    req_trans = requests.get(url=f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/"
                                                 f"uzb-muhammadsodikmu/{surah}/{ayah}.json")
                    data_trans = req_trans.json()
                    text_trans = data_trans['text']
                    max_length = 950
                    chunks = [text_trans[i:i + max_length] for i in range(0, len(text_trans), max_length)]
                    if len(text_trans) >= max_length:
                        text_1 = chunks[0]
                        text_2 = chunks[1]
                        await bot.send_audio(chat_id=message.chat.id, audio=req_audio.content,
                                             caption=f"{surah_name} surasi {ayah} - oyat 📖\n\n"
                                                     f"👇👇 Tarjimasi 👇👇\n\n<code>{text_1}</code>\n\n",
                                             parse_mode="HTML")
                        await bot.send_message(chat_id=message.chat.id, text=f"<code>{text_2}</code>\n\n"
                                                                             f"<a href='{bot_link}'>{bot_nick}</a>🤖\n"
                                                                             f"<a href='{link}'>{creator}</a>🧑‍💻",
                                               parse_mode="HTML")
                    else:
                        await bot.send_audio(chat_id=message.chat.id, audio=req_audio.content,
                                             caption=f"{surah_name} surasi {ayah} - oyat 📖\n\n"
                                                     f"👇👇 Tarjimasi 👇👇\n\n<code>{text_trans}</code>\n\n"
                                                     f"<a href='{bot_link}'>{bot_nick}</a>🤖\n"
                                                     f"<a href='{link}'>{creator}</a>🧑‍💻",
                                             parse_mode="HTML")
                else:
                    await bot.send_message(chat_id=message.chat.id,
                                           text="Ma'lumotlar mos kelmadi!")
    else:
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=sent_msg.message_id,
                                    text="Iltimos, sura va oyat raqamini 1:5 ( sura:oyat ) formatida yuboring!")
