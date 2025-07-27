from sqlalchemy import select, or_, delete, union_all
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import aliased
from models import User, Reaction, Payment, Cache, Gender, PaymentType
from typing import Any, Optional
from db_connect import AsyncSessionLocal
import aiohttp
from languages import get_texts
from config import *


# TODO бан пользователя


__all__ = ['save_to_cache',
           'get_cached_message_id',
           'delete_from_cache',
           'create_or_update_user',
           'update_user_fields',
           'get_user_by_id',
           'add_reaction',
           'add_payment',
           'get_location_info',
           'find_first_matching_user',
           'get_caption',
           'get_gender_label',
           'get_gender_search_label',
           'delete_user_by_id',
           'get_location_opencage',
           'get_match_targets',
           'get_collection_targets',
           'get_intent_targets',
           'get_prev_next_ids',
           ]


async def find_first_matching_user(current_user_id: int) -> Optional[User]:
    async with AsyncSessionLocal() as session:
        # ПОИСК. Получаем первого подходящего пользователя
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
            User.incognito_switch == False,
            User.banned == False,
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


async def get_caption(user: User, lang: str = None, reaction: str = None) -> str:
    # получить описание для пользователя
    if lang and reaction:
        texts = await get_texts(lang)
        reaction_str = texts["BUTTONS_TEXT"]["reaction"][reaction]
        caption=(f"<b>{user.first_name}</b>"
        f"\n📌 {user.country_local}, {user.city_local}"
        f"\n<i>{texts["TEXT"]["match_menu"]["you_want"].format(reaction=reaction_str)}</i>"
        f"\n\n<i>{user.about_me}</i>")
    else:
        caption=(f"<b>{user.first_name}</b>"
        f"\n📌 {user.country_local}, {user.city_local}"
        f"\n\n<i>{user.about_me}</i>")
    
    return caption


async def get_gender_label(gender: Gender, lang: str) -> str:
    texts = await get_texts(lang)
    return texts['GENDER_LABELS'][gender]


async def get_gender_search_label(gender: Gender, lang: str) -> str:
    texts = await get_texts(lang)
    return texts['GENDER_SEARCH_LABELS'][gender]


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


# Удалить запись из кэша по параметру
# await delete_from_cache(user_id, "start_message_id")
async def delete_from_cache(user_id: int, parameter: str) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Cache).where(
                Cache.telegram_id == user_id,
                Cache.parameter == parameter
            )
        )
        cache_entry = result.scalar_one_or_none()

        if cache_entry:
            await session.delete(cache_entry)
            await session.commit()


# Функция для создания или обновления пользователя
# Пример:
# await create_or_update_user(user_id, first_name, username)
async def create_or_update_user(user_id: int, first_name: str, username: str) -> User:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=user_id,
                first_name=first_name,
                username=username
            )
            session.add(user)
        else:
            if user.first_name != first_name:
                user.first_name = first_name
            if user.username != username:
                user.username = username
            # session.add(user) не нужен — объект уже в сессии

        await session.commit()
        return user


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


# Удаление пользователя по telegram_id
async def delete_user_by_id(user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        # Удаляем связанные записи в кэше
        await session.execute(delete(Cache).where(Cache.telegram_id == user_id))
        await session.execute(delete(Reaction).where(Reaction.telegram_id == user_id))
        await session.execute(delete(Payment).where(Payment.telegram_id == user_id))
        
        # Удаляем самого пользователя
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True


# Добавление реакции в базу
async def add_reaction(user_id: int, target_tg_id: int, reaction_str: str):
    async with AsyncSessionLocal() as session:
        stmt = insert(Reaction).values(
            telegram_id=user_id,
            target_tg_id=target_tg_id,
            reaction=reaction_str
        ).on_conflict_do_update(
            index_elements=['telegram_id', 'target_tg_id'],
            set_={'reaction': reaction_str}
        )
        await session.execute(stmt)
        await session.commit()



# Добавление платежа в базу
async def add_payment(user_id: int, amount: int, payment_type: PaymentType, target_id: int | None = None):
    async with AsyncSessionLocal() as session:
        payment = Payment(
            telegram_id=user_id,
            target_tg_id=target_id,
            amount=amount,
            type=payment_type
        )
        session.add(payment)
        await session.commit()


# -----------------------------------------------------------------геолокация ------------------------------------------------------


async def get_location_opencage(latitude: float, longitude: float, lang: str = 'en') -> str:
    api_key = opencagedata_API_KEY
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": f"{latitude},{longitude}",
        "key": api_key,
        "language": lang
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            try:
                components = data["results"][0]["components"]
                city = components.get("city") or components.get("town") or components.get("village") or "Unknown city"
                country = components.get("country", "Unknown country")
                return country, city
            except (IndexError, KeyError):
                return "Location not found"
            

# Запасная
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


# ----------------------------------------------------------------- совпадения ------------------------------------------------------


# Найти Совпадения match
# Возращает  словарь {id: reaction} и кол-во
async def get_match_targets(user_id: int) -> tuple[dict[int, str], int]:
    async with AsyncSessionLocal() as session:
        user_reactions = aliased(Reaction)
        target_reactions = aliased(Reaction)

        result = await session.execute(
            select(user_reactions.target_tg_id, user_reactions.reaction)
            .join(
                target_reactions,
                (user_reactions.target_tg_id == target_reactions.telegram_id) &
                (user_reactions.telegram_id == target_reactions.target_tg_id) &
                (user_reactions.reaction == target_reactions.reaction)
            )
            .where(
                user_reactions.telegram_id == user_id,
                user_reactions.reaction != "SKIP"  # <-- исключаем SKIP
            )
        )

        matches = dict(sorted(result.all(), key=lambda x: x[0]))
        return matches, len(matches)


# Получить из Коллекции
async def get_collection_targets(user_id: int) -> tuple[list[int], int]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Payment.target_tg_id)
            .where(Payment.telegram_id == user_id, Payment.target_tg_id != None)
        )
        ids = result.scalars().unique().all()
        sorted_ids = sorted(ids)
        return sorted_ids, len(ids)


# Найти по намерениям, исключая взаимных и тех, кто в Коллекции
async def get_intent_targets(user_id: int, intent: str) -> tuple[list[int], int]:
    async with AsyncSessionLocal() as session:
        # Подзапрос: пользователи, которым я поставил эту же реакцию (взаимные)
        subq_mutual = (
            select(Reaction.target_tg_id)
            .where(
                Reaction.telegram_id == user_id,
                Reaction.reaction == intent.upper()
            )
        )

        # Подзапрос: пользователи, которым я поставил SKIP
        subq_skipped = (
            select(Reaction.target_tg_id)
            .where(
                Reaction.telegram_id == user_id,
                Reaction.reaction == "SKIP"
            )
        )

        # Подзапрос: пользователи, кого я оплатил
        subq_collection = (
            select(Payment.target_tg_id)
            .where(
                Payment.telegram_id == user_id,
                Payment.target_tg_id != None
            )
        )

        # Объединённый подзапрос: исключаем всех из этих 3 подгрупп
        union_subq = union_all(subq_mutual, subq_skipped, subq_collection).subquery()

        # Основной запрос: те, кто мне поставил intent, но не попал в исключения
        result = await session.execute(
            select(Reaction.telegram_id)
            .where(
                Reaction.target_tg_id == user_id,
                Reaction.reaction == intent.upper(),
                ~Reaction.telegram_id.in_(select(union_subq.c.target_tg_id))
            )
        )

        ids = result.scalars().unique().all()
        sorted_ids = sorted(ids)
        return sorted_ids, len(ids)


# Найти id-до и id-после в списке
async def get_prev_next_ids(current_id: int, ids: list[int]) -> tuple[int | None, int | None]:
    try:
        index = ids.index(current_id)
        prev_id = ids[index - 1] if index > 0 else None
        next_id = ids[index + 1] if index < len(ids) - 1 else None
        return prev_id, next_id
    except ValueError:
        return None, None


# возврат id если не None
async def pick_id(ids: list[int | None]) -> tuple[int | str, str | int, str | int]:
    back_id, next_id = ids
    chosen = next_id or back_id or "None"
    return chosen, back_id, next_id

