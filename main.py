import logging
import aiohttp
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_API_KEY, ADMIN_ID, MONGO_DB_PASSWORD, MONGO_DB_USERNAME

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

# ------------------------------------------------------------------- Команды -------------------------------------------------------

# Команда старт
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    print(f'Запись в базу: {user_id}, {user_name}')
    await message.answer(f"Привет, {user_name}!\nГотов к новым знакомствам?\n\nЧтобы начать нужно выполнить несколько простых шагов\nШаг 1. Подтверди что тебе есть 18 лет\nШаг 2. Отправь мне свое местоположение\nШаг 3. Укажи свой пол \nШаг 4. Кого ты ищешь? \nШаг 5. Отправь свое фото")
    button = InlineKeyboardButton(text="Мне больше 18 лет", callback_data="18yes")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Шаг 1. Подтверди что тебе есть 18 лет\nПо законам многих стран, чтобы пользоваться сервисами подобным нашего тебе должно быть больше 18 лет.\nДай свое согласие, что ты понимаешь все риски и уже достиг нужного возраста",
                         reply_markup=markup)

@dp.callback_query(F.data == "18yes")
async def to_query(callback: types.CallbackQuery):
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
    await message.delete() #удалить сообщение пользователя с локацией
    latitude = message.location.latitude
    longitude = message.location.longitude

    # 1. Получаем название на языке пользователя (по языку Telegram)
    user_language_code = message.from_user.language_code or 'ru'
    country_local, city_local = await get_location_info(latitude, longitude, lang=user_language_code)

    # 2. Получаем название на английском для записи в базу
    country_en, city_en = await get_location_info(latitude, longitude, lang='en')

    # Пример записи в базу (здесь просто выводим)
    print(f"В базу сохраняем: {city_en}, {country_en}")

    # Отправляем пользователю локализованный ответ
    await message.answer(
        f"✅ Шаг 2 выполнен\nТы находишься в:\nГород: {city_local}\nСтрана: {country_local}",
        reply_markup=ReplyKeyboardRemove()
    )
    button1 = InlineKeyboardButton(text="Мужчина", callback_data="man")
    button2 = InlineKeyboardButton(text="Женщина", callback_data="woman")
    button3 = InlineKeyboardButton(text="Другое", callback_data="any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    await message.answer("Шаг 3. Укажи свой пол", reply_markup=markup)


@dp.callback_query(F.data.in_(["man", "woman", "any"]))
async def to_query2(callback: types.CallbackQuery):
    await callback.answer(text=f"Отлично! Ты указал, что ты {callback.data}")
    await callback.message.edit_text(text="✅ Шаг 3 выполнен")
    button1 = InlineKeyboardButton(text="Ищу Мужчину", callback_data="search_man")
    button2 = InlineKeyboardButton(text="Ищу Женщину", callback_data="search_woman")
    button3 = InlineKeyboardButton(text="Пол не имеет значения", callback_data="search_any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    await callback.message.answer("Шаг 4. Укажи кото ты ищешь", reply_markup=markup)


@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def to_query3(callback: types.CallbackQuery):
    await callback.answer(text=f"Отлично! Ты указал, что ты ищешь {callback.data}")
    await callback.message.edit_text(text="✅ Шаг 4 выполнен")
    await callback.message.answer("Шаг 5. Отправь свое фото", reply_markup=ReplyKeyboardRemove())


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    print(f"Сохраняем file_id в базу: {file_id}")
    await message.delete()
    await message.answer("✅ Шаг 5 выполнен\nСпасибо! Анкета заполнена. Скоро начнём поиск собеседников.")


async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())