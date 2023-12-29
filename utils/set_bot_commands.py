from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Botdan foydalanish"),
            types.BotCommand("search_ayah", "Oyat izlash"),
            types.BotCommand("search_surah", "Sura izlash"),
            types.BotCommand("sajda_ayahs", "Sajda oyatlari"),
            types.BotCommand("prayer_times", "Namoz vaqtlari"),
            types.BotCommand("search_hadith", "Hadis izlash")
        ]
    )
