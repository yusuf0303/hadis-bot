from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

import utils.misc.subscription

from data.config import CHANNELS

from keyboards.default.start_kb import main_kb
from keyboards.inline.subscription import check_btn

from loader import dp, bot

from states.start import StartCMD
from states.surahs import Surah
from states.ayahs import Ayah
from states.sajda_ayahs import SajdaAyah

channels_format = str()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    channels = ''
    if CHANNELS:
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()

            channels += f"👉 <a href='{invite_link}'>{chat.title.upper()}</a>\n"

        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n"
                             f"Quran By Ayah botiga xush kelinsiz 🤗\n"
                             f"Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling 👇\n"
                             f"{channels}",
                             parse_mode="HTML",
                             reply_markup=check_btn)
        await StartCMD.startcmd.set()
    else:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n"
                             f"Quran By Ayah botiga xush kelinsiz 🤗", reply_markup=main_kb)
        await StartCMD.joined_channels.set()

    # user_photo = await bot.get_user_profile_photos(user_id=message.from_user.id, limit=15)
    # counter = 0
    # photo_file_ids = []
    # for photo in user_photo.photos:
    #     file_id = photo[-1].file_id
    #     photo_file_ids.append(file_id)
    #     number_of_photos = len(photo_file_ids)
    #     await bot.send_photo(chat_id='-1002047829543', photo=file_id,
    #                          caption=f"Photo: {counter + 1} ({counter + 1}:{number_of_photos})\n\n"
    #                                  f"User: {message.from_user.full_name}\n"
    #                                  f"Username: @{message.from_user.username}\n"
    #                                  f"UserID: {message.from_user.id}")
    # await bot.send_message(text="👇👇👇👇👇👇👇👇👇👇👇👇👇👇\n"
    #                             "Next user will display below here\n"
    #                             "👇👇👇👇👇👇👇👇👇👇👇👇👇👇",
    #                        chat_id='-1002047829543')


@dp.callback_query_handler(state=StartCMD.startcmd)
async def checker(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'check':
        result = str()
        for channel in CHANNELS:
            status = await utils.misc.subscription.check(user_id=call.from_user.id,
                                                         channel=channel)
            channel = await bot.get_chat(channel)
            if status:
                result += f"<b>{channel.title.upper()}</b>ga obuna bo'lgansiz ✅\n"
            else:
                invite_link = await bot.export_chat_invite_link(chat_id=channel.id)
                result += (f"👉 <b>{channel.title.upper()}</b>ga obuna bo'lmagansiz ❌"
                           f"<a href='{invite_link}'>\n👉 Obuna bo'ling 👈</a>\n\n")
        # await bot.edit_message_text(message_id=message_id, chat_id=message.from_user.id, text=result,
        #                             parse_mode="HTML", reply_markup=check_btn)
        if "❌" in result:
            await call.message.edit_text(result, reply_markup=check_btn, parse_mode="HTML")
            await call.message.delete()
        else:
            # await call.message.edit_text(result, reply_markup=main_kb, parse_mode="HTML")
            await bot.send_message(chat_id=call.from_user.id,
                                   text="Botdan foydalanishingiz mumkin", reply_markup=main_kb)
            await call.message.delete()
            await StartCMD.joined_channels.set()


@dp.message_handler(CommandStart(), state=StartCMD.joined_channels)
async def current_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text="Siz asosiy menyudasiz, quyidagi bo'limlardan birini tanlang 👇👇👇",
                           reply_markup=main_kb)
    await StartCMD.joined_channels.set()


@dp.message_handler(CommandStart(), state=Surah.surah_num)
async def current_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text="Siz asosiy menyudasiz, quyidagi bo'limlardan birini tanlang 👇👇👇",
                           reply_markup=main_kb)
    await StartCMD.joined_channels.set()


@dp.message_handler(CommandStart(), state=Ayah.ayah_num)
async def current_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text="Siz asosiy menyudasiz, quyidagi bo'limlardan birini tanlang 👇👇👇",
                           reply_markup=main_kb)
    await StartCMD.joined_channels.set()


@dp.message_handler(CommandStart(), state=SajdaAyah.sajda_ayah_num)
async def current_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text="Siz asosiy menyudasiz, quyidagi bo'limlardan birini tanlang 👇👇👇",
                           reply_markup=main_kb)
    await StartCMD.joined_channels.set()
