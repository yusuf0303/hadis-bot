from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, bot

from states.start import StartCMD
from states.surahs import Surah
from states.ayahs import Ayah
from states.hadiths import Hadith


@dp.message_handler(CommandHelp(), state=StartCMD.joined_channels)
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Botdan foydalanish",
            "/search_ayah - Oyat izlash",
            "/search_surah - Sura izlash",
            "/sajda_ayahs - Sajda oyatlari",
            "/prayer_times - Namoz vaqtlari",
            "/search_hadis - Hadis izlash"
            )
    
    await message.answer("\n".join(text))


@dp.message_handler(CommandHelp(), state=Surah.surah_num)
async def surah_help(message: types.Message):
    with open("handlers/users/images/surahs.jpg", 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption="Suralarni olish uchun suraning tartib raqamini yuboring.\n"
                                     "Suralar tartibi suratda ko'rsatilgan 👆")


@dp.message_handler(CommandHelp(), state=Ayah.ayah_num)
async def ayah_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Oyat izlash uchun sura raqami va oyat raqamini misolda ko'rsatilgandek kiriting\n"
                                "Misol: Fotiha surasining 5-oyatini olish uchun 👉 1:5\n\n"
                                "Sura va oyat raqamlari : bilan ajratib yozilishi kerak.")


@dp.message_handler(CommandHelp(), state=Hadith.hadith_state)
async def hadith_help(message: types.Message):
    with open("handlers/users/images/profile_image.jpg", 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption="Quyidagi bo'limlardan birini tanlang yoki kerakli hadis raqamini yuboring 👇")
