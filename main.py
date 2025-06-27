import logging
import aiohttp
import random
from enum import Enum
from aiogram.types import InputMediaPhoto, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_API_KEY, ADMIN_ID, MONGO_DB_PASSWORD, MONGO_DB_USERNAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Reaction, Buy
from test_db import test_db


# ------------------------------------------------------------------- Настройка и активация бота -------------------------------------------------------

# TODO Supabase - SQL bd Postgres


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Создание подключения и сессии
engine = create_engine("sqlite:///my_database.db")
Session = sessionmaker(bind=engine)
session = Session()



class ReactionType(str, Enum):
    LOVE = "LOVE"
    SEX = "SEX"
    CHAT = "CHAT"
    SKIP = "SKIP"

    @property
    def label(self):
        return {
            self.LOVE: "Свидание",
            self.SEX: "Постель",
            self.CHAT: "Общение",
            self.SKIP: "Пропуск",
        }[self]

    @property
    def message_template(self):
        return {
            self.LOVE: "Ты лайкнул {name}",
            self.SEX: "Ты лайкнул {name}",
            self.CHAT: "Ты лайкнул {name}",
            self.SKIP: "Ты пропустил {name}",
        }[self]


# ------------------------------------------------------------------- Функции -------------------------------------------------------


# Получить данные о местоположении с указанным языком
async def get_location_info(latitude, longitude, lang='en'):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "accept-language": lang
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            address = data.get("address", {})
            country = address.get("country")
            city = address.get("city") or address.get("town") or address.get("village")
            return country, city
        

async def get_random_user():
    random_user = random.choice(test_db)
    target_tg_id = random_user.get('tg_id', 0)
    target_name = random_user.get('name', '')
    description = random_user.get('description', '')
    photo_id = random_user.get('photo_id', '')
    caption=f"<b>{target_name}</b>\n<i>{description}</i>"

    button1 = InlineKeyboardButton(text="☕ Свидание", callback_data=f"reaction|LOVE|{target_name}|{target_tg_id}")
    button2 = InlineKeyboardButton(text="👩‍❤️‍💋‍👨 Постель", callback_data=f"reaction|SEX|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="💬 Общение", callback_data=f"reaction|CHAT|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="Пропустить ⏩", callback_data=f"reaction|SKIP|{target_name}|{target_tg_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1, button2, button3], [button4]])
    
    return photo_id, caption, markup


async def get_matches_menu_buttons():
    menu_picture = "AgACAgIAAxkBAAICVmhbrdh8xXXGx6Xy1tr0ouQN0sjFAAIZ8DEbBk3hSoeHxcGbNuBQAQADAgADeQADNgQ"

    button0 = InlineKeyboardButton(text=f"💘 Совпадения [{random.randint(0, 1000)}]", callback_data=f"matches")
    button1 = InlineKeyboardButton(text=f"Свидание [{random.randint(0, 1000)}]", callback_data=f"who_wants|LOVE")
    button2 = InlineKeyboardButton(text=f"Постель [{random.randint(0, 1000)}]", callback_data=f"who_wants|SEX")
    button3 = InlineKeyboardButton(text=f"Общение [{random.randint(0, 1000)}]", callback_data=f"who_wants|CHAT")
    button4 = InlineKeyboardButton(text=f"Обновить 🔄", callback_data=f"reload_matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button0], [button1, button2, button3], [button4],])
    
    return menu_picture, markup


async def get_wants_user(reaction, price):
    if reaction == "love":
        pass
    elif reaction == "sex":
        pass
    elif reaction == "chat":
        pass
    
    random_user = random.choice(test_db)
    target_tg_id = random_user.get('tg_id', 0)
    target_name = random_user.get('name', '')
    target_username = random_user.get('username', '')
    description = random_user.get('description', '')
    photo_id = random_user.get('photo_id', '')
    caption=f"<b>{target_name}</b>\n<i>{description}</i>"


    button1 = InlineKeyboardButton(text=f"Добавить в Совпадения {price} ⭐️", callback_data=f"wants_pay|{target_name}|{target_tg_id}|{price}", pay=True)
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"wants_back|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"wants_next|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])

    return photo_id, caption, markup


async def get_matches_user():
    random_user = random.choice(test_db)
    target_tg_id = random_user.get('tg_id', 0)
    target_name = random_user.get('name', '')
    target_username = random_user.get('username', '')
    description = random_user.get('description', '')
    photo_id = random_user.get('photo_id', '')
    caption=f"<b>{target_name}</b>\n<i>{description}</i>"

    button1 = InlineKeyboardButton(text="✉️ Начать знакомство", callback_data=f"matches_chat|{target_name}|{target_tg_id}", url=f"https://t.me/{target_username}")
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"matches_back|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"matches_next|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return photo_id, caption, markup


# ------------------------------------------------------------------- Команды -------------------------------------------------------


# Команда поиск
@dp.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    photo_id, caption, markup = await get_random_user()
    await message.answer_photo(photo=photo_id, caption=caption, parse_mode="HTML", reply_markup=markup)


# Команда Совпадения
@dp.message(Command("match"))
async def cmd_match(message: types.Message, state: FSMContext):
    menu_picture, markup = await get_matches_menu_buttons()
    await message.answer_photo(photo=menu_picture, parse_mode="HTML", reply_markup=markup)


# Команда старт
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    if username == None:
        await message.answer("""
⚠️ Для использования бота необходимо установить username в Telegram.

Как это сделать:
1️⃣ Откройте Telegram → Настройки → Имя пользователя (tg://settings/username)
2️⃣ Придумайте уникальное Имя пользователя
3️⃣ Сохрани ✅

После этого вернись в бота \nи нажми 👉 /start , чтобы продолжить регистрацию.
""")
    else:
        # запись в базу
        new_user = User(telegram_id=user_id, first_name=first_name, username=username)
        session.add(new_user)
        session.commit()
        session.close()

        await message.answer(f"Привет, {first_name}!\nГотов к новым знакомствам?\n\nЧтобы начать нужно выполнить несколько простых шагов:\n\nШаг 1. Подтверди что тебе есть 18 лет\nШаг 2. Отправь свое местоположение\nШаг 3. Укажи свой пол \nШаг 4. Кого ты ищешь? \nШаг 5. Отправь свое фото\nШаг 6. Расскажи коротко о себе")
        button = InlineKeyboardButton(text="Мне больше 18 лет", callback_data="18yes")
        markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
        await message.answer("👉 Шаг 1. Подтверди, что тебе есть 18 лет\n\n"
                             "<i>По законам многих стран, чтобы пользоваться сервисами, подобными нашему, тебе должно быть больше 18 лет.</i>\n\n"
                             "Дай своё согласие, что ты понимаешь все риски и уже достиг нужного возраста.",
                             reply_markup=markup,
                             parse_mode="HTML")


# ------------------------------------------------------------------- Колбеки -------------------------------------------------------


gender = {"MAN": "Мужчина", "WOMAN": "Женщина", "ANY": "Другое"}
gender_search = {"search_man": "Ищу Мужчину", "search_woman": "Ищу Женщину", "search_any": "Пол не имеет значения"}
gender_search_db = {"search_man": "MAN", "search_woman": "WOMAN", "search_any": "ANY"}


@dp.callback_query(F.data == "18yes")
async def query_18years(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # запись в базу
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.eighteen_years_old = True
    session.commit()
    session.close()

    await callback.answer(text="Отлично! Ты подтвердил, что тебе больше 18 лет")

    # 1. Меняем текст сообщения и убираем inline-кнопки
    await callback.message.edit_text(text="✅ Шаг 1 выполнен")

    # 2. Отдельно отправляем сообщение с обычной клавиатурой для геолокации
    kb = [[types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажми на кнопку"
    )
    await callback.message.answer(
        "👉 Шаг 2. Отправь мне свое местоположение\n\n" \
        "Теперь нужно определить, где ты находишься. Поиск производится среди людей из того же города, что и ты.\n\n"
        "<i>Если вы используете десктоп/ПК вам необходимо авторизоваться на мобильном устройстве, чтобы выполнить этот этап</i>",
        reply_markup=keyboard, parse_mode="HTML")


# Принимаем локацию
@dp.message(F.location)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    await message.delete() #удалить сообщение пользователя с локацией
    latitude = message.location.latitude
    longitude = message.location.longitude

    # 1. Получаем название на языке пользователя (по языку Telegram)
    user_language_code = message.from_user.language_code or 'ru'
    country_local, city_local = await get_location_info(latitude, longitude, lang=user_language_code)

    # 2. Получаем название на английском для записи в базу
    country_en, city_en = await get_location_info(latitude, longitude, lang='en')

    # запись в базу
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.country = country_en
    user.city = city_en
    session.commit()
    session.close()

    # Отправляем пользователю локализованный ответ
    await message.answer(
        f"✅ Шаг 2 выполнен\nТы находишься в:\nГород: {city_local}\nСтрана: {country_local}",
        reply_markup=ReplyKeyboardRemove()
    )
    button1 = InlineKeyboardButton(text="Мужчина", callback_data="MAN")
    button2 = InlineKeyboardButton(text="Женщина", callback_data="WOMAN")
    button3 = InlineKeyboardButton(text="Другое", callback_data="ANY")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    await message.answer("👉 Шаг 3. Укажи свой пол", reply_markup=markup)


@dp.callback_query(F.data.in_(["MAN", "WOMAN", "ANY"]))
async def query_gender(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # запись в базу
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.gender = callback.data
    session.commit()
    session.close()

    await callback.answer(text=f"Отлично! Ты указал: {gender.get(callback.data)}")
    await callback.message.edit_text(text="✅ Шаг 3 выполнен")
    button1 = InlineKeyboardButton(text="Ищу Мужчину", callback_data="search_man")
    button2 = InlineKeyboardButton(text="Ищу Женщину", callback_data="search_woman")
    button3 = InlineKeyboardButton(text="Пол не имеет значения", callback_data="search_any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    await callback.message.answer("👉 Шаг 4. Укажи кото ты ищешь", reply_markup=markup)


@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def query_gender_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    # запись в базу
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.gender_search = gender_search_db.get(callback.data)
    session.commit()
    session.close()

    await callback.answer(text=f"Отлично! Ты указал: {gender_search.get(callback.data)}")
    await callback.message.edit_text(text="✅ Шаг 4 выполнен")
    await callback.message.answer("👉 Шаг 5. Отправь свое фото 📷", reply_markup=ReplyKeyboardRemove())


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_id = photo.file_id

    # запись в базу
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.photo_id = file_id
    session.commit()
    session.close()

    await message.delete()
    await message.answer("✅ Шаг 5 выполнен")
    await message.answer("👉 Шаг 6. Расскажи коротко о себе\n<i>Постарайся уложиться в 2-3 строки</i>", parse_mode="HTML")


# обработка колбека поиска
@dp.callback_query(lambda c: c.data.startswith("reaction"))
async def handle_reaction(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, reaction_str, target_name, target_tg_id = callback.data.split("|", 3)

    try:
        reaction = ReactionType(reaction_str)
    except ValueError:
        await callback.answer("Неизвестная реакция")
        return

    # запись в базу
    new_reaction = Reaction(telegram_id=user_id, target_tg_id=target_tg_id, reaction=reaction_str)
    session.add(new_reaction)
    session.commit()
    session.close()

    await callback.answer(reaction.message_template.format(name=target_name))

    photo_id, caption, markup = await get_random_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(F.data == "matches")
async def query_matches(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    photo_id, caption, markup = await get_matches_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(F.data == "matches_menu")
async def query_matches_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    menu_picture, markup = await get_matches_menu_buttons()
    await callback.message.edit_media(media=InputMediaPhoto(media=menu_picture))
    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(F.data == "reload_matches_menu")
async def query_reload_matches_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, markup = await get_matches_menu_buttons()
    await callback.message.edit_reply_markup(reply_markup=markup)


# обработка колбека кому нравишься
@dp.callback_query(lambda c: c.data.startswith("who_wants"))
async def handle_who_wants(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, reaction = callback.data.split("|", 1)
    photo_id, caption, markup = await get_wants_user(reaction, 10)
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


# ------------------------------------------------------------------- Оплата -------------------------------------------------------

def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить через Telegram Stars ⭐️", pay=True)
    return builder.as_markup()


# обработка колбека оплаты
@dp.callback_query(lambda c: c.data.startswith("wants_pay"))
async def handle_wants_pay(callback: types.CallbackQuery):
    _, target_name, target_tg_id, price_str = callback.data.split("|")
    price = int(price_str)

    prices = [LabeledPrice(label=f"Добавить {target_name} в Совпадения", amount=price)]

    await callback.message.answer_invoice(
        title=f"Добавить в Совпадения {target_name}",
        description=f"При добавлении в Совпадения, вы получите доступ к профилю человека и сможете ему написать",
        payload=f"match_{target_tg_id}",
        provider_token="YOUR_PROVIDER_TOKEN",  # <-- сюда токен из BotFather
        currency="XTR",
        prices=prices,
        reply_markup=payment_keyboard()
    )

    await callback.answer() 


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(lambda message: message.successful_payment is not None)
async def on_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id

    # Пример обработки payload:
    if payload.startswith("match_"):
        target_id = payload.split("_")[1]
        # ✅ Добавить в совпадения
        await message.answer(f"✅ Вы добавили пользователя с ID {target_id} в Совпадения!")


# ------------------------------------------------------------------- Текст -------------------------------------------------------


# обработка текста - добавляет или изменяет описание "о себе"
@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    await message.delete()
    text = message.text
    print(text)
    if len(text) <= 110:

        # запись в базу
        user = session.query(User).filter_by(telegram_id=user_id).first()
        user.about_me = text
        session.commit()
        session.close()

        await message.answer("✅ Шаг 6 выполнен")
        await message.answer("🔍 Найти партнера - /search" \
        "\n💘Совпадения (match) - /match")
    else:
        await message.answer("❌ Шаг 6 не выполнен. Количество символов превышает лимит в 110 символов. Попробуй еще раз")


# ------------------------------------------------------------------- Активация бота -------------------------------------------------------


async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())