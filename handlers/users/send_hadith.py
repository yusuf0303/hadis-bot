import random

from aiogram import types

from loader import dp, bot
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from states.hadiths import Hadith
from states.start import StartCMD

from keyboards.default.start_kb import main_kb
from keyboards.default.hadith_kb import menu_keyboard


@dp.message_handler(commands=['search_hadith'])
@dp.message_handler(Text(equals="Hadis izlash"), state=StartCMD.joined_channels)
async def hadith_cmd(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Hadislar bo'limiga xush kelibsiz 🤗\n"
                                "Ushbu bo'limdagi barcha hadislar @Mishkotulmasobiyh kanalidan olingan",
                           reply_markup=menu_keyboard)
    await Hadith.hadith_state.set()


@dp.message_handler(Text(equals="Menyuga qaytish"), state=Hadith.hadith_state)
async def get_surah_num(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text="Asosiy menyuga qaytdingiz!",
                           reply_markup=main_kb)
    await state.finish()
    await StartCMD.joined_channels.set()


creator = 'Created By SmartCoder'
link = "https://t.me/R_Yusuf_Bot"
bot_nick = "Surah By Ayah Bot"
bot_link = "https://t.me/test_132_robot"


not_found = ['3', '31', '51', '99', '169', '172', '187', '192', '224', '226', '229', '231', '233', '241', '264',
             '278', '283', '313', '322', '328', '372', '379', '380', '403', '458', '496', '532', '534', '573',
             '610', '639', '655', '690', '711', '722', '735', '816', '850', '852', '951', '976', '1010', '1270',
             '1271', '1272', '1314', '1329', '1331', '1372', '1373', '1390', '1399', '1414', '1474', '1487']


@dp.message_handler(Text(equals="Muallif 👤"), state=Hadith.hadith_state)
async def send_author_cmd(message: types.Message):
    await bot.send_audio(chat_id=message.chat.id,
                         audio=f"https://t.me/mishkat_ull/{117}",
                         caption=f"Муаллиф Ҳақида\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                 f"@Mishkotulmasobiyh\n\n"
                                 f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                 f"<a href='{link}'>{creator}</a>",
                         parse_mode="HTML")


@dp.message_handler(Text(equals="Muqaddima 🗒️"), state=Hadith.hadith_state)
async def send_info_auth(message: types.Message):
    await bot.send_audio(chat_id=message.chat.id,
                         audio=f"https://t.me/mishkat_ull/{118}",
                         caption=f"Муаллиф муқаддимаси\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                 f"@Mishkotulmasobiyh\n\n"
                                 f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                 f"<a href='{link}'>{creator}</a>",
                         parse_mode="HTML")


@dp.message_handler(Text(equals="Tasodifiy 🧾"), state=Hadith.hadith_state)
async def send_rand(message: types.Message):
    rand_hadith = random.randint(119, 1620)
    if str(rand_hadith - 117) in not_found:
        await bot.send_message(chat_id=message.chat.id, text=f"{rand_hadith} - ҳадис топилмади!"
                                                             f"'Тасодифий ҳадис 🧾'ни қайта босинг 👇")
        await message.delete()
    else:
        await bot.send_audio(chat_id=message.chat.id,
                             audio=f"https://t.me/mishkat_ull/{rand_hadith}",
                             caption=f"{rand_hadith - 117} - Ҳадис\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                     f"@Mishkotulmasobiyh\n\n"
                                     f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                     f"<a href='{link}'>{creator}</a>",
                             parse_mode="HTML")


@dp.message_handler(Text(equals="n-hadis 🧾"), state=Hadith.hadith_state)
async def send_n_cmd(message: types.Message):
    with open("handlers/users/images/profile_image.jpg", 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption="1 дан 1500 гача ихтиёрий битта сон юборинг! 👇")


@dp.message_handler(state=Hadith.hadith_state)
async def send_num_hadith(message: types.Message):
    for char in message.text:
        ascii_value = ord(char)
        if 48 <= ascii_value <= 57:
            if int(message.text) <= 0:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"{message.text} - Ҳадис мавжуд эмас!")
                break
            elif message.text in not_found:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"{message.text} сўрови бўйича Ҳадис топилмади!")
                break
            elif 0 < int(message.text) < 3:
                num = int(message.text) + 118
                await bot.send_audio(chat_id=message.chat.id,
                                     audio=f"https://t.me/mishkat_ull/{num}",
                                     caption=f"{message.text} - Ҳадис\nТинглаш 👉 00:00\n\n"
                                             f"Каналга уланиш учун \n👇👇👇\n"
                                             f"@Mishkotulmasobiyh\n\n"
                                             f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                             f"<a href='{link}'>{creator}</a>",
                                     parse_mode="HTML")
                break
            elif 3 < int(message.text) <= 1500:
                num = int(message.text) + 117
                await bot.send_audio(chat_id=message.chat.id,
                                     audio=f"https://t.me/mishkat_ull/{num}",
                                     caption=f"{message.text} - Ҳадис\nТинглаш 👉 00:00\n\n"
                                             f"Каналга уланиш учун \n👇👇👇\n"
                                             f"@Mishkotulmasobiyh\n\n"
                                             f"<a href='{bot_link}'>{bot_nick}</a>\n"
                                             f"<a href='{link}'>{creator}</a>",
                                     parse_mode="HTML")
                break
            else:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"{message.text} - Ҳадис Ин Шаа Aллоҳ енди қўшилади!")
                break
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Faqatgina hadisning tartib raqamini yuboring!")
            break
