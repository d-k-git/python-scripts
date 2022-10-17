# Bot helper fragment for refugee women from Ukraine

# pip install aiogram
import sys
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, \
    InlineKeyboardButton, InlineKeyboardMarkup
#   CallbackQuery, KeyboardButton

from config import TOKEN_KEY

#photo = open('logo.png', 'rb')

#sys.path.append('../../')

#logging.basicConfig(level=logging.INFO)

TOKEN = TOKEN_KEY
print(TOKEN)
bot = Bot(TOKEN)
dp = Dispatcher(bot)



from aiohttp import ClientSession

from config import MEASUREMENT_ID, API_SECRET


async def send_analytics(user_id, user_lang_code, action_name):
    """
    Send record to Google Analytics
    """
    params = {
        'client_id': str(user_id),
        'user_id': str(user_id),
        'events': [{
            'name': action_name,
            'params': {
                'language': user_lang_code,
                'engagement_time_msec': '1',
            }
        }],
    }
    async with ClientSession() as session:
        await session.post(
                f'https://www.google-analytics.com/'
                f'mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}',
                json=params)



# Пишем команду с приветствием и заставкой
@dp.message_handler(commands=['start'])
async def callback_start(message: Message):
    #await bot.send_photo(chat_id=message.chat.id, photo=open('logo.png', 'rb').read())
    await bot.send_photo(chat_id=message.chat.id, photo='https://raw.githubusercontent.com/d-k-git/tg-bot/main/logo.png')
    #await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile.from_url('logo.png'))
    await bot.send_message(
        chat_id=message.chat.id,
        reply_markup=choose_lang,
        text="Привет, я справочный чат-бот. Помогу вам. Выберите язык:")

# Пишем команду с приветствием и заставкой
@dp.message_handler(commands=['language'])
async def callback_language(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        reply_markup=choose_lang,
        text="Выберите язык:")

    await send_analytics(user_id=message.from_user.id,
                         user_lang_code=message.from_user.language_code,
                         action_name='select_lang_rus')

# Создаем первую клавиатуру c выбором языка
choose_lang = InlineKeyboardMarkup().row(
    InlineKeyboardButton(text="Українськa", callback_data="get-UKR"),
    InlineKeyboardButton(text="Русский", callback_data="get-RUS"))


# Указываем, что сделать при нажатии на кнопку после выбора языка:
@dp.callback_query_handler(lambda c: c.data == 'get-UKR')
async def get_UKR(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=chosen_ukr,
        text="Виберіть країну:")

    await send_analytics(user_id=message.from_user.id,
                         user_lang_code=message.from_user.language_code,
                         action_name='select_lang_ukr')

@dp.callback_query_handler(lambda c: c.data == 'get-RUS')
async def get_RUS(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=chosen_rus,
        text="Выберите страну:")


# --------- ЗДЕСЬ ВЫБОР СТРАНЫ И РАЗДЕЛА ---------
chosen_rus = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Германия", callback_data="DEU_rus"),
    InlineKeyboardButton(text="Польша", callback_data="POL_rus"),
)
chosen_ukr = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Німеччина", callback_data="DEU_ukr"),
    InlineKeyboardButton(text="Польща", callback_data="POL_ukr"),
)


# ------- Доступные разделы по стране: ГЕРМАНИЯ -------
DEU_chosen_service_rus = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Безопасность", callback_data="DEU_sec_main_rus"),
)

DEU_chosen_service_ukr = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Безпека", callback_data="DEU_sec_main_ukr"),
)


# ------- Доступные разделы по стране: ПОЛЬША -------
POL_chosen_service_rus = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Безопасность", callback_data="POL_sec_main_rus"),
    InlineKeyboardButton(text="Медицина", callback_data="POL_med_main_rus"),
    InlineKeyboardButton(text="Работа", callback_data="POL_wrk_main_rus"),
    InlineKeyboardButton(text="Проживание", callback_data="POL_res_main_rus"),
    InlineKeyboardButton(text="Юридическая помощь", callback_data="POL_law_main_rus"),
    InlineKeyboardButton(text="Бытовые вопросы", callback_data="POL_day_main_rus"),
)

POL_chosen_service_ukr = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Безпека", callback_data="POL_sec_main_ukr"),
    InlineKeyboardButton(text="Медицина", callback_data="POL_med_main_ukr"),
    InlineKeyboardButton(text="Робота", callback_data="POL_wrk_main_ukr"),
    InlineKeyboardButton(text="Проживання", callback_data="POL_res_main_ukr"),
    InlineKeyboardButton(text="Юридична допомога", callback_data="POL_law_main_ukr"),
    InlineKeyboardButton(text="Побутові питання", callback_data="POL_day_main_ukr"),
)


@dp.callback_query_handler(lambda c: c.data == "DEU_rus")
async def DEU_rus(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=DEU_chosen_service_rus,
        text="Выберите вид помощи:")

    await send_analytics(user_id=message.from_user.id,
                         user_lang_code=message.from_user.language_code,
                         action_name='DEU_chosen_service_rus')

@dp.callback_query_handler(lambda c: c.data == "POL_rus")
async def POL_rus(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=POL_chosen_service_rus,
        text="Выберите вид помощи:")

    await send_analytics(user_id=message.from_user.id,
                     user_lang_code=message.from_user.language_code,
                     action_name='POL_chosen_service_rus')


@dp.callback_query_handler(lambda c: c.data == "DEU_ukr")
async def DEU_ukr(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=DEU_chosen_service_ukr,
        text="Виберіть вид допомоги:")
    await send_analytics(user_id=message.from_user.id,
                     user_lang_code=message.from_user.language_code,
                     action_name='DEU_chosen_service_ukr')


@dp.callback_query_handler(lambda c: c.data == "POL_ukr")
async def POL_ukr(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        reply_markup=POL_chosen_service_ukr,
        text="Виберіть вид допомоги:")


# --------- ЗДЕСЬ ДЕРЕВО ПО РАЗДЕЛАМ И СТРАНАМ ---------
# ------- РАЗДЕЛ: БЕЗОПАСНОСТЬ -------
# ----- СТРАНА: ГЕРМАНИЯ -----
# --- Кнопка БЕЗОПАСНОСТЬ : "Безопасность" ---
# - Язык русский -
# Клавиатура:
DEU_sec_main_rus_buttons = InlineKeyboardMarkup(row_width=1)
DEU_sec_main_rus_buttons = DEU_sec_main_rus_buttons.add(
    InlineKeyboardButton(text=(
        "Другие варианты поддержки"),
                         callback_data="DEU_sec_other_rus"),
    InlineKeyboardButton(text=(
        "Как себя обезопасить"),
                         callback_data="DEU_sec_selfprotect_rus"),
    InlineKeyboardButton(text=(
        "Как распознать сутенёра и узнать, легальна ли работа"),
                         callback_data="DEU_sec_illegal_rus"),
    InlineKeyboardButton(text=(
        "Список ресурсов для помощи беженцам"),
                         callback_data="DEU_sec_general_rus"),
    )
DEU_sec_main_rus_buttons = DEU_sec_main_rus_buttons.row(
    InlineKeyboardButton(text=(
        "🗂 К разделам"), callback_data="DEU_rus"),
    InlineKeyboardButton(text=(
        "🌍 Другая страна"), callback_data="get-RUS"),
    InlineKeyboardButton(text=(
        "🆘 SOS"), callback_data="DEU_sec_main_rus"))


[...]


# --------- ЗДЕСЬ ЗАКАНЧИВАЕТСЯ ДЕРЕВО ПО РАЗДЕЛАМ И СТРАНАМ ---------


if __name__ == "__main__":
    # dp.register_message_handler(DEU_sec_other_rus, state="*")
    executor.start_polling(dp)
