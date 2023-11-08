
import random
import datetime

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text

from config import TOKEN
from keyboards import main_menu

bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Bot is running successfully ✅\nCreated by SmartCoder🧑‍💻")

help_msg = """
<em>/start - Ботни қайта ишга тушириш</em>
<em>/help - Ёрдамчи буйруқлар</em>
<em>/off - Ботни тўхтатиш</em>
<em>/muallif - Муаллиф ҳақида</em>
<em>/muqaddima - Муқаддима ҳақида</em>
"""

start_date = datetime.datetime(2023, 11, 8).date()
current_date = datetime.datetime.now().date()
worked_days = (current_date - start_date).days

users = []
users_removed = []
usernames = []
all_users = []


@dp.message_handler(commands=['add'])
async def send_msg_to_users(message: types.Message):
    if message.chat.id == 579386059:
        for user in users:
            await bot.send_message(chat_id=user,
                                   text="Ботдаги янгиликлардан фойдаланиш учун /start "
                                        "командаси орқали уни қайта ишга туширинг")


async def check_user(message: types.Message):
    if message.chat.id not in users:
        users.append(message.chat.id)
        usernames.append(message.chat.username)
        print("User successfully added ✅")
    else:
        print("User has already added ✅")


async def send_data(message: types.Message):
    datas = {
        'user_id': message.chat.id,
        'Ism': message.from_user.first_name,
        'username': message.from_user.username,
        'numUser': len(users)
    }
    data = (f"New user 👤\nUser ID: {datas['user_id']}\nUser Fullname: {datas['Ism']}\nUsername: @{datas['username']}\n"
            f"Number of Users: {datas['numUser']}")
    await bot.send_message(chat_id=579386059,
                           text=data)
    private_data = (f"New user 👤\nUser ID: {datas['user_id']}\nUser Fullname: {datas['Ism']}\n"
                    f"Username: @{datas['username']}\n"
                    f"Number of Users: {datas['numUser']}")
    all_users.append(private_data)


@dp.message_handler(Text(equals="Муаллиф 👤"))
async def author_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        await bot.send_audio(chat_id=message.chat.id,
                             audio=f"https://t.me/mishkat_ull/{117}",
                             caption="Муаллиф Ҳақида\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                     "@Mishkotulmasobiyh"
                                     "\n\nCreated by SmartCoder🧑‍💻")


@dp.message_handler(Text(equals="Муқаддима 🗒️"))
async def author_info_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        await bot.send_audio(chat_id=message.chat.id,
                             audio=f"https://t.me/mishkat_ull/{118}",
                             caption="Муаллиф муқаддимаси\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                     "@Mishkotulmasobiyh\n\nCreated by SmartCoder🧑‍💻")

not_found = ['3', '31', '51', '99', '169', '172', '187', '192', '224', '226', '229', '231', '233', '241', '264',
             '278', '283', '313', '322', '328', '372', '379', '380', '403', '458', '496', '532', '534', '573',
             '610', '639', '655', '690', '711', '722', '735', '816', '850', '852', '951', '976', '1010', '1270',
             '1271', '1272', '1314', '1329', '1331', '1372', '1373', '1390', '1399', '1414', '1474', '1487']


@dp.message_handler(Text(equals="Тасодифий ҳадис 🧾"))
async def rand_hadith_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        rand_hadith = random.randint(119, 1620)
        print(rand_hadith)
        if str(rand_hadith - 117) in not_found:
            await bot.send_message(chat_id=message.chat.id, text=f"{rand_hadith} - ҳадис топилмади!"
                                                                 f"'Тасодифий ҳадис 🧾'ни қайта босинг 👇")
            await message.delete()
        else:
            await bot.send_audio(chat_id=message.chat.id,
                                 audio=f"https://t.me/mishkat_ull/{rand_hadith}",
                                 caption=f"{rand_hadith - 117} - Ҳадис\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                         f"@Mishkotulmasobiyh\n\nCreated by SmartCoder🧑‍💻")


@dp.message_handler(Text(equals="n-чи ҳадис 🧾"))
async def n_hadith_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        with open("./images/profile_image.jpg", 'rb') as photo:
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo,
                                 caption="1 дан 1500 гача ихтиёрий битта сон юборинг! 👇")


@dp.message_handler(Text(equals="Бот статистикаси 📊"))
async def info_bot_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        with open("./images/profile_image.jpg", 'rb') as photo:
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo,
                                 caption=f"Бот ишга тушган сана: {start_date}📅\n"
                                         f"Бугунги сана: {current_date}🗓️\n"
                                         f"Ишга тушганига: {worked_days} кун бўлди📅\n"
                                         f"Обуначилар сони: {len(users)}👥")


async def welcome_cmd(message: types.Message):
    if message.chat.id not in users:
        await message.answer(f"Aссалому алайкум,\n{message.from_user.full_name}! \n@Mishkotulmasobiyh каналининг "
                             f"расмий ботига хуш келибсиз😊\n\nБотдан фойдаланишда қуйидаги буйруқлардан "
                             f"фойдаланишингиз мумкин👇\n\nМуаллиф ҳақида маълумот олиш учун\n👉 /Muallif"
                             f"\nМуқаддима билан танишиш учун\n👉 /Muqaddima\nҲадис излаш учун ҳадис рақамини 1 дан "
                             f"1500 гача киритинг\nУмумий ёрдам 👉 /help\nОбунани тўхтатиш 👉 /off")
        await bot.send_message(chat_id=message.chat.id,
                               text="Ўз шахсий ботингиз бўлишини истасйсизми?\n"
                                    "👉 @R_Yusuf_030305 👈\nMурожаат қилинг",
                               reply_markup=main_menu)
        await check_user(message)
        await send_data(message)
    else:
        await message.answer(f"Aссалому алайкум,\n{message.from_user.full_name}! \n@Mishkotulmasobiyh каналининг "
                             f"расмий ботига хуш келибсиз😊\n\nБотдан фойдаланишда қуйидаги буйруқлардан "
                             f"фойдаланишингиз мумкин👇\n\nМуаллиф ҳақида маълумот олиш учун\n👉 /Muallif"
                             f"\nМуқаддима билан танишиш учун\n👉 /Muqaddima\nҲадис излаш учун ҳадис рақамини 1 дан "
                             f"1500 гача киритинг\nУмумий ёрдам 👉 /help\nОбунани тўхтатиш 👉 /off")
        await bot.send_message(chat_id=message.chat.id,
                               text="Want to have your own bot?\nThen contact 👇\n@R_Yusuf_030305",
                               reply_markup=main_menu)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if message.chat.id in users_removed:
        users_removed.remove(message.chat.id)
        await welcome_cmd(message)
    else:
        await welcome_cmd(message)


@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    if message.chat.id in users:
        await bot.send_message(chat_id=message.chat.id,
                               text=help_msg,
                               parse_mode="HTML")
        await check_user(message)


@dp.message_handler(commands=['off'])
async def off_cmd(message: types.Message):
    if message.chat.id in users:
        await bot.send_message(chat_id=message.chat.id,
                               text="Бот муваффақиятли тўхтатилди ✅")
        if message.chat.id in users:
            users_removed.append(message.chat.id)
            users.remove(message.chat.id)
            print("User successfully removed ✅")

        datas = {
            'user_id': message.chat.id,
            'Ism': message.from_user.first_name,
            'username': message.from_user.username,
            'numUser': len(users)
        }
        data = (f"User left👤\nUser ID: {datas['user_id']}\nUser Fullname: {datas['Ism']}\n"
                f"Username: @{datas['username']}\n"
                f"Number of Users: {datas['numUser']}")
        await bot.send_message(chat_id=579386059,
                               text=data)


@dp.message_handler(commands=['muallif'])
async def author_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        await bot.send_audio(chat_id=message.chat.id,
                             audio=f"https://t.me/mishkat_ull/{117}",
                             caption="Муаллиф Ҳақида\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                     "@Mishkotulmasobiyh\n\nCreated by SmartCoder🧑‍💻")


@dp.message_handler(commands=['muqaddima'])
async def muqaddima_cmd(message: types.Message):
    if message.chat.id in users:
        await check_user(message)
        await bot.send_audio(chat_id=message.chat.id,
                             audio=f"https://t.me/mishkat_ull/{118}",
                             caption="Муаллиф муқаддимаси\nТинглаш 👉 00:00\n\nКаналга уланиш учун \n👇👇👇\n"
                                     "@Mishkotulmasobiyh\n\nCreated by SmartCoder🧑‍💻")


@dp.message_handler(commands=['users'])
async def author_cmd(message: types.Message):
    if message.chat.id == 579386059:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Active users 👇\n{all_users}")
        await bot.send_message(chat_id=message.chat.id,
                               text=f"Removed users 👇\n{users_removed}")


@dp.message_handler()
async def num_hadith_cmd(message: types.Message):
    if message.chat.id in users:
        for char in message.text:
            ascii_value = ord(char)
            if 48 <= ascii_value <= 57:
                if int(message.text) < 0:
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
                                                 f"@Mishkotulmasobiyh\n\nCreated by SmartCoder🧑‍💻")
                    break
                elif 3 < int(message.text) <= 1500:
                    num = int(message.text) + 117
                    await bot.send_audio(chat_id=message.chat.id,
                                         audio=f"https://t.me/mishkat_ull/{num}",
                                         caption=f"{message.text} - Ҳадис\nТинглаш 👉 00:00\n\n"
                                                 f"Каналга уланиш учун \n👇👇👇\n"
                                                 f"@Mishkotulmasobiyh\n\nCreated by SmartCoder🧑‍💻")
                    break
                else:
                    await bot.send_message(chat_id=message.chat.id,
                                           text=f"{message.text} - Ҳадис Ин Шаа Aллоҳ енди қўшилади!")
                    break
            else:
                await bot.send_message(chat_id=message.chat.id,
                                       text="Faqatgina hadisning tartib raqamini yuboring!")
                break

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
