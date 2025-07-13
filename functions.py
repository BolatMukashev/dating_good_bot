from sqlalchemy import select, update, or_
from sqlalchemy.orm import aliased
from models import User, Reaction, Payment, Cache, Gender
from typing import Any, Optional
from db_connect import AsyncSessionLocal
import aiohttp
from messages import supported_languages, GENDER_LABELS, GENDER_SEARCH_LABELS
from sqlalchemy.orm import aliased


__all__ = ['save_to_cache',
           'get_cached_message_id',
           'create_or_update_user',
           'update_user_fields',
           'get_user_by_id',
           'add_reaction',
           'add_payment',
           'get_location_info',
           'get_user_language',
           'find_first_matching_user',
           'get_caption',
           'get_gender_label',
           'get_gender_search_label']


async def find_first_matching_user(current_user_id: int) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        # Получаем текущего пользователя
        result = await session.execute(
            select(User).where(User.telegram_id == current_user_id)
        )
        current_user = result.scalar_one_or_none()
        if not current_user:
            return None

        gender = current_user.gender
        gender_search = current_user.gender_search

        # Кого ты ищешь
        gender_condition = or_(
            User.gender == gender_search,
            gender_search == Gender.ANY
        )

        # Подходишь ли ты им
        if gender == Gender.ANY:
            search_condition = User.gender_search == Gender.ANY
        else:
            search_condition = or_(
                User.gender_search == gender,
                User.gender_search == Gender.ANY
            )

        # Исключаем инкогнито
        not_incognito_condition = or_(
            User.incognito_switch == False,
            User.incognito_pay == False
        )

        # Исключаем тех, на кого уже реагировал
        ReactionAlias = aliased(Reaction)
        subquery = select(ReactionAlias.target_tg_id).where(
            ReactionAlias.telegram_id == current_user_id
        )

        # Общие условия
        base_conditions = [
            User.telegram_id != current_user_id,
            gender_condition,
            search_condition,
            not_incognito_condition,
            User.telegram_id.not_in(subquery)
        ]

        # 👉 Шаг 1: сначала ищем по стране и городу
        query_city = select(User).where(
            *base_conditions,
            User.city == current_user.city,
            User.country == current_user.country
        ).limit(1)

        result = await session.execute(query_city)
        match = result.scalar_one_or_none()
        if match:
            return match

        # 👉 Шаг 2: если не нашли в городе — ищем по стране
        query_country = select(User).where(
            *base_conditions,
            User.country == current_user.country
        ).limit(1)

        result = await session.execute(query_country)
        match = result.scalar_one_or_none()
        if match:
            return match

        # 👉 Шаг 3: совсем никого
        return None


async def get_caption(user: User) -> str:
    # получить описание для пользователя
    caption=(f"<b>{user.first_name}</b>"
    f"\n📌 {user.country_local}, {user.city_local}"
    f"\n⚤ {user.gender.value}, {user.gender_search.value}"
    f"\n<i>{user.about_me}</i>")
    return caption


async def get_gender_label(gender: Gender, lang: str = "ru") -> str:
    return GENDER_LABELS[lang][gender]


async def get_gender_search_label(gender: Gender, lang: str = "ru") -> str:
    return GENDER_SEARCH_LABELS[lang][gender]


# сохранить любое значение Кэш с параметром
# Пример:
# await save_to_cache(user_id, "start_message_id", starting_message.message_id)
# await save_to_cache(callback.from_user.id, "invoice_message_id", sent_invoice.message_id)
async def save_to_cache(user_id: int, parameter: str, message_id: int = None) -> None:
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
        else:
            new_cache = Cache(
                telegram_id=user_id,
                parameter=parameter,
                message_id=message_id
            )
            session.add(new_cache)

        await session.commit()


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


# Получение информации о пользователе
async def get_user_by_id(user_id: int) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        return user


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
