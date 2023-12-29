from aiogram import types
import requests

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters import Text

from states.prayer_times import PrayerTime
from states.start import StartCMD

from loader import dp, bot

from keyboards.default.regions import regions, back_region
from keyboards.default.start_kb import main_kb


@dp.message_handler(Command('prayer_times'), state=StartCMD.joined_channels)
@dp.message_handler(Text(equals="Namoz vaqtlari"), state=StartCMD.joined_channels)
async def get_region(message: types.Message, state: FSMContext):
    await message.answer("Hududingizni tanlang!",
                         reply_markup=regions)
    await PrayerTime.region.set()


@dp.message_handler(Text(equals="Menyuga qaytish 🔝"), state=PrayerTime.region)
async def go_home(message: types.Message, state: FSMContext):
    await message.answer("Asosiy menyuga qaytdingiz!",
                         reply_markup=main_kb)
    await state.finish()
    await StartCMD.joined_channels.set()


@dp.message_handler(Text(equals="Nukus ( Qoraqalpog'iston Res )"), state=PrayerTime.region)
async def get_time(message: types.Message, state: FSMContext):
    nukus = message.text.rstrip(" ( Qoraqalpog'iston Res )") + 's'
    await message.answer(f"<b><i>{nukus}  ( Qoraqalpog'iston Res )</i></b> uchun namoz vaqtlaridan birini tanlang",
                         reply_markup=back_region,
                         parse_mode="HTML")
    await state.update_data(
        {'region': nukus}
    )
    await PrayerTime.prayer_time_lim.set()


@dp.message_handler(state=PrayerTime.region)
async def get_reg_time(message: types.Message, state: FSMContext):
    reg_names = []
    for row in regions.keyboard:
        for btn in row:
            reg_names.append(btn.text)
    if message.text in reg_names:
        await message.answer(f"<b><i>{message.text} viloyati (shahri)</i></b> uchun namoz vaqtlaridan birini tanlang",
                             reply_markup=back_region,
                             parse_mode="HTML")
        await state.update_data(
            {'region': message.text}
        )
        await PrayerTime.prayer_time_lim.set()
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Hududlardan birini tanlang 👇👇👇",
                               reply_markup=regions)


@dp.message_handler(Text(equals="⬅️ Orqaga"), state=PrayerTime.prayer_time_lim)
async def go_back(message: types.Message, state: FSMContext):
    await message.answer("Hududingizni tanlang!",
                         reply_markup=regions)
    await state.finish()
    await PrayerTime.region.set()


@dp.message_handler(Text(equals="Menyuga qaytish 🔝"), state=PrayerTime.prayer_time_lim)
async def go_home(message: types.Message, state: FSMContext):
    await message.answer("Asosiy menyuga qaytdingiz!",
                         reply_markup=main_kb)
    await state.finish()
    await StartCMD.joined_channels.set()


@dp.message_handler(Text(equals="Bomdod 🌅"), state=PrayerTime.prayer_time_lim)
async def bomdod_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    fajr = req['times']['tong_saharlik']
    sunrise = req['times']['quyosh']
    day = req['weekday']
    date = req['date']

    bot_link = f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>"
    creator = f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"
    await message.answer(f"<code>{region} - uchun Bomdod namozi vaqti!\n\n"
                         f"Hafta kuni: {day}\nSana: {date}\n\n"
                         f"👉 Bomdod (Saharlik): {fajr}\n"
                         f"👉 Quyosh chiqishi: {sunrise}</code>\n\n"
                         f"{bot_link}\n{creator}",
                         parse_mode="HTML",
                         reply_markup=back_region)


@dp.message_handler(Text(equals="Peshin 🕑"), state=PrayerTime.prayer_time_lim)
async def peshin_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    peshin = req['times']['peshin']
    day = req['weekday']
    date = req['date']

    bot_link = f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>"
    creator = f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"
    await message.answer(f"<code>{region} - uchun Peshin namozi vaqti!\n\n"
                         f"Hafta kuni: {day}\nSana: {date}\n\n"
                         f"👉 Peshin: {peshin}</code>\n\n"
                         f"{bot_link}\n{creator}",
                         parse_mode="HTML",
                         reply_markup=back_region)


@dp.message_handler(Text(equals="Asr 🌇"), state=PrayerTime.prayer_time_lim)
async def asr_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    asr = req['times']['asr']
    day = req['weekday']
    date = req['date']

    bot_link = f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>"
    creator = f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"
    await message.answer(f"<code>{region} - uchun Asr namozi vaqti!\n\n"
                         f"Hafta kuni: {day}\nSana: {date}\n\n"
                         f"👉 Asr: {asr}</code>\n\n"
                         f"{bot_link}\n{creator}",
                         parse_mode="HTML",
                         reply_markup=back_region)


@dp.message_handler(Text(equals="Shom 🌆"), state=PrayerTime.prayer_time_lim)
async def shom_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    shom = req['times']['shom_iftor']
    day = req['weekday']
    date = req['date']

    bot_link = f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>"
    creator = f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"
    await message.answer(f"<code>{region} - uchun Shom namozi vaqti!\n\n"
                         f"Hafta kuni: {day}\nSana: {date}\n\n"
                         f"👉 Shom (Iftorlik): {shom}</code>\n\n"
                         f"{bot_link}\n{creator}",
                         parse_mode="HTML",
                         reply_markup=back_region)


@dp.message_handler(Text(equals="Xufton 🌃"), state=PrayerTime.prayer_time_lim)
async def xufton_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    hufton = req['times']['hufton']
    day = req['weekday']
    date = req['date']

    bot_link = f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>"
    creator = f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"
    await message.answer(f"<code>{region} - uchun Xufton namozi vaqti!\n\n"
                         f"Hafta kuni: {day}\nSana: {date}\n\n"
                         f"👉 Xufton: {hufton}</code>\n\n"
                         f"{bot_link}\n{creator}",
                         parse_mode="HTML",
                         reply_markup=back_region)


@dp.message_handler(Text(equals="Bugun ( To'liq ) 📅"), state=PrayerTime.prayer_time_lim)
async def today_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/day?region={region}").json()
    day = req['weekday']
    date = req['date']
    fajr = req['times']['tong_saharlik']
    sunrise = req['times']['quyosh']
    peshin = req['times']['peshin']
    asr = req['times']['asr']
    shom = req['times']['shom_iftor']
    hufton = req['times']['hufton']

    msg_text = (f"<code>{region} - uchun bugungi namoz vaqtlari!\n\n"
                f"Hafta kuni: {day}\nSana: {date}\n\n"
                f"👉 Bomdod (Saharlik): {fajr}\n"
                f"👉 Quyosh chiqishi: {sunrise}\n"
                f"👉 Peshin: {peshin}\n"
                f"👉 Asr: {asr}\n"
                f"👉 Shom: {shom}\n"
                f"👉 Xufton: {hufton}</code>\n\n")

    msg_text += f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>\n"
    msg_text += f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"
    await message.answer(text=msg_text,
                         parse_mode="HTML",
                         reply_markup=back_region)


@dp.message_handler(Text(equals="Shu hafta ( To'liq ) 🗓️"), state=PrayerTime.prayer_time_lim)
async def this_week_cmd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    region = data.get('region')
    req = requests.get(url=f"https://islomapi.uz/api/present/week?region={region}").json()
    full_caption = ''
    for item in req:
        date_time = item['date']
        date_part = date_time.split(",")[0]

        region = item['region']
        weekday = item['weekday']
        times = item['times']

        caption = f"<code><b>👇👇 Hudud: {region} 👇👇</b>\n" \
                  f"Namoz vaqtlari: <b>{date_part}</b>\n" \
                  f"Quyosh chiqishi: <b>{times['quyosh']}</b>\n\n" \
                  f"Hafta kuni: <b>{weekday}</b>\n"
        for key, value in times.items():
            caption += f"👉 {key.capitalize()}: <b>{value}</b>\n"

        caption += "</code>\n\n"
        full_caption += caption
    full_caption += f"<a href='https://t.me/test_132_robot'>Quran By Ayah Bot 🤖</a>\n"
    full_caption += f"<a href='https://t.me/R_Yusuf_Bot'>Created by SmartCoder 🧑‍💻</a>"

    await bot.send_message(chat_id=message.chat.id,
                           text=full_caption,
                           parse_mode="HTML",
                           reply_markup=back_region)


@dp.message_handler(state=PrayerTime.prayer_time_lim)
async def other_cmd(message: types.Message, state: FSMContext):
    await message.answer(text="Iltimos, quyidagi bo'limlardan birini tanlang 👇",
                         reply_markup=back_region)
