from sqlalchemy import select, update
from models import Base, User, Reaction, Payment, Cache
from typing import Any
from db_connect import AsyncSessionLocal
import aiohttp
from messages import supported_languages


# получать id сообщения в бд Кэш по параметру
# Пример:
# start_message_id = await get_cached_message_id(user_id, "start_message_id")
async def get_cached_message_id(user_id: int, parameter: str) -> int | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Cache).where(
                Cache.telegram_id == user_id,
                Cache.parameter == parameter
            )
        )
        cache_entry = result.scalar_one_or_none()
        return cache_entry.message_id if cache_entry else None


# получать текст в бд Кэш по параметру
# Пример:
# city_local = await get_cached_data(user_id, "city_local")
async def get_cached_data(user_id: int, parameter: str) -> str | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Cache).where(
                Cache.telegram_id == user_id,
                Cache.parameter == parameter
            )
        )
        cache_entry = result.scalar_one_or_none()
        return cache_entry.data if cache_entry else None


# сохранить любое значение Кэш с параметром
# Пример:
# await save_to_cache(user_id, "start_message_id", starting_message.message_id)
# await save_to_cache(callback.from_user.id, "invoice_message_id", sent_invoice.message_id)
async def save_to_cache(user_id: int, parameter: str, message_id: int = None, data: str = None) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Cache).where(
                Cache.telegram_id == user_id,
                Cache.parameter == parameter
            )
        )
        existing_cache = result.scalar_one_or_none()

        if existing_cache:
            if message_id is not None:
                existing_cache.message_id = message_id
                existing_cache.data = None  # очищаем data
            elif data is not None:
                existing_cache.data = data
                existing_cache.message_id = None  # очищаем message_id
        else:
            new_cache = Cache(
                telegram_id=user_id,
                parameter=parameter,
                message_id=message_id if message_id is not None else None,
                data=data if data is not None else None
            )
            session.add(new_cache)

        await session.commit()



# Функция для создания или обновления пользователя
# Пример:
# await create_or_update_user(user_id, first_name, username)
async def create_or_update_user(user_id: int, first_name: str, username: str) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            new_user = User(
                telegram_id=user_id,
                first_name=first_name,
                username=username
            )
            session.add(new_user)
        else:
            updated = False
            if existing_user.first_name != first_name:
                existing_user.first_name = first_name
                updated = True
            if existing_user.username != username:
                existing_user.username = username
                updated = True
            if updated:
                session.add(existing_user)

        await session.commit()


# Универсальная функция обновления полей пользователя
# Примеры:
# await update_user_fields(user_id, first_name="Алиса", username="alisa2025", is_active=True)
# await update_user_fields(user_id, eighteen_years_old=True)
async def update_user_fields(user_id: int, **fields: Any) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).filter_by(telegram_id=user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return False  # пользователь не найден

        updated = False
        for field, value in fields.items():
            if hasattr(user, field) and getattr(user, field) != value:
                setattr(user, field, value)
                updated = True

        if updated:
            await session.commit()

        return updated


# Добавление реакции в базу
async def add_reaction(user_id: int, target_tg_id: int, reaction_str: str):
    async with AsyncSessionLocal() as session:
        new_reaction = Reaction(telegram_id=user_id, target_tg_id=target_tg_id, reaction=reaction_str)
        session.add(new_reaction)
        await session.commit()


# Добавление платежа в базу
async def add_payment(user_id: int, target_tg_id: int, price: int):
    async with AsyncSessionLocal() as session:
        payment = Payment(telegram_id=user_id, target_tg_id=target_tg_id, price=price)
        session.add(payment)
        await session.commit()


async def get_location_info(latitude, longitude, lang='en'):
    # Получить данные о местоположении с указанным языком
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
        

async def get_user_language(message):
    # получить язык пользователя, иначе - английский
    user_lang = message.from_user.language_code
    if user_lang not in supported_languages:
        user_lang = 'en'
    return user_lang



