import logging
import aiohttp
import random
from aiogram.types import InputMediaPhoto
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_API_KEY, ADMIN_ID, MONGO_DB_PASSWORD, MONGO_DB_USERNAME
from test_db import test_db


# ------------------------------------------------------------------- Настройка и активация бота -------------------------------------------------------


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


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

    button1 = InlineKeyboardButton(text="☕ Свидание", callback_data=f"reaction_love|{target_name}|{target_tg_id}")
    button2 = InlineKeyboardButton(text="👩‍❤️‍💋‍👨 Постель", callback_data=f"reaction_sex|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="💬 Общение", callback_data=f"reaction_chat|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="Пропустить ⏩", callback_data=f"reaction_skip|{target_name}|{target_tg_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1, button2, button3], [button4]])
    
    return photo_id, caption, markup


# ------------------------------------------------------------------- Команды -------------------------------------------------------


# Команда поиск
@dp.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    photo_id, caption, markup = await get_random_user()
    await message.answer_photo(photo=photo_id, caption=caption, parse_mode="HTML", reply_markup=markup)


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
        print(f'Запись в базу: {user_id}, {first_name}, {username}')
        await message.answer(f"Привет, {first_name}!\nГотов к новым знакомствам?\n\nЧтобы начать нужно выполнить несколько простых шагов:\n\nШаг 1. Подтверди что тебе есть 18 лет\nШаг 2. Отправь свое местоположение\nШаг 3. Укажи свой пол \nШаг 4. Кого ты ищешь? \nШаг 5. Отправь свое фото\nШаг 6. Расскажи коротко о себе")
        button = InlineKeyboardButton(text="Мне больше 18 лет", callback_data="18yes")
        markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
        await message.answer("👉 Шаг 1. Подтверди, что тебе есть 18 лет\n\n"
                             "<i>По законам многих стран, чтобы пользоваться сервисами, подобными нашему, тебе должно быть больше 18 лет.</i>\n\n"
                             "Дай своё согласие, что ты понимаешь все риски и уже достиг нужного возраста.",
                             reply_markup=markup,
                             parse_mode="HTML")


# ------------------------------------------------------------------- Колбеки -------------------------------------------------------


gender = {"man": "Мужчина", "woman": "Женщина", "any": "Другое"}
gender_choice = {"search_man": "Ищу Мужчину", "search_woman": "Ищу Женщину", "search_any": "Пол не имеет значения"}

@dp.callback_query(F.data == "18yes")
async def to_query(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    print(f'Запись в базу: {user_id} Есть 18 - True')
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
        "👉 Шаг 2. Отправь мне свое местоположение\nТеперь нужно определить, где ты находишься. Поиск производится среди людей из того же города, что и ты.",
        reply_markup=keyboard)


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

    # Пример записи в базу (здесь просто выводим)
    print(f"Запись в базу: {user_id} расположение {city_en}, {country_en}")

    # Отправляем пользователю локализованный ответ
    await message.answer(
        f"✅ Шаг 2 выполнен\nТы находишься в:\nГород: {city_local}\nСтрана: {country_local}",
        reply_markup=ReplyKeyboardRemove()
    )
    button1 = InlineKeyboardButton(text="Мужчина", callback_data="man")
    button2 = InlineKeyboardButton(text="Женщина", callback_data="woman")
    button3 = InlineKeyboardButton(text="Другое", callback_data="any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    await message.answer("👉 Шаг 3. Укажи свой пол", reply_markup=markup)


@dp.callback_query(F.data.in_(["man", "woman", "any"]))
async def to_query2(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    print(f'Запись в базу: {user_id} выбрал пол {callback.data}')
    await callback.answer(text=f"Отлично! Ты указал, что ты {gender.get(callback.data)}")
    await callback.message.edit_text(text="✅ Шаг 3 выполнен")
    button1 = InlineKeyboardButton(text="Ищу Мужчину", callback_data="search_man")
    button2 = InlineKeyboardButton(text="Ищу Женщину", callback_data="search_woman")
    button3 = InlineKeyboardButton(text="Пол не имеет значения", callback_data="search_any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    await callback.message.answer("👉 Шаг 4. Укажи кото ты ищешь", reply_markup=markup)


@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def to_query3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    print(f'Запись в базу: {user_id} находится в поиске {callback.data}')
    await callback.answer(text=f"Отлично! Ты указал, что ты ищешь {gender_choice.get(callback.data)}")
    await callback.message.edit_text(text="✅ Шаг 4 выполнен")
    await callback.message.answer("👉 Шаг 5. Отправь свое фото 📷", reply_markup=ReplyKeyboardRemove())


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_id = photo.file_id
    print(f"Запись в базу: {user_id} file_id фотографии {file_id}")
    await message.delete()
    await message.answer("✅ Шаг 5 выполнен")
    await message.answer("👉 Шаг 6. Расскажи коротко о себе")


# обработка колбека поиска, свидание
@dp.callback_query(lambda c: c.data.startswith("reaction_love|"))
async def handle_reaction_love(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("|", 2)
    target_name = parts[1]
    target_tg_id = parts[2]
    print(f'Запись в базу: {user_id} реакция Свидание на {target_tg_id}')
    await callback.answer(text=f"Ты лайкнул {target_name}")

    photo_id, caption, markup = await get_random_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


# обработка колбека поиска, постель
@dp.callback_query(lambda c: c.data.startswith("reaction_sex|"))
async def handle_reaction_sex(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("|", 2)
    target_name = parts[1]
    target_tg_id = parts[2]
    print(f'Запись в базу: {user_id} реакция Постель на {target_tg_id}')
    await callback.answer(text=f"Ты лайкнул {target_name}")

    photo_id, caption, markup = await get_random_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


# обработка колбека поиска, общение
@dp.callback_query(lambda c: c.data.startswith("reaction_chat|"))
async def handle_reaction_chat(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("|", 2)
    target_name = parts[1]
    target_tg_id = parts[2]
    print(f'Запись в базу: {user_id} реакция Общение на {target_tg_id}')
    await callback.answer(text=f"Ты лайкнул {target_name}")

    photo_id, caption, markup = await get_random_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


# обработка колбека поиска, пропустить
@dp.callback_query(lambda c: c.data.startswith("reaction_skip|"))
async def handle_reaction_skip(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("|", 2)
    target_name = parts[1]
    target_tg_id = parts[2]
    print(f'Запись в базу: {user_id} реакция Пропуск на {target_tg_id}')
    await callback.answer(text=f"Ты пропустил {target_name}")

    photo_id, caption, markup = await get_random_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, parse_mode="HTML")
    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    await message.delete()
    text = message.text
    print(f"Запись в базу: {user_id} добавил описание {text}")
    await message.answer("✅ Шаг 6 выполнен")
    await message.answer("Чтобы начать поиск собеседника, нажми на кнопку: /search")


async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())