from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, User, Reaction, Payment, Cache
from typing import Any
from db_connect import AsyncSessionLocal


# получать любое значение Кэш по параметру
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

# Пример:
# start_message_id = await get_cached_message_id(user_id, "start_message_id")


# сохранить любое значение Кэш с параметром
async def save_to_cache(user_id: int, parameter: str, message_id: int) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Cache).where(
                Cache.telegram_id == user_id,
                Cache.parameter == parameter
            )
        )
        existing_cache = result.scalar_one_or_none()

        if existing_cache:
            existing_cache.message_id = message_id
        else:
            new_cache = Cache(
                telegram_id=user_id,
                parameter=parameter,
                message_id=message_id
            )
            session.add(new_cache)

        await session.commit()

# Пример:
# await save_to_cache(user_id, "start_message_id", starting_message.message_id)
# await save_to_cache(callback.from_user.id, "invoice_message_id", sent_invoice.message_id)


# Функция для создания или обновления пользователя
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

# Пример:
# await create_or_update_user(user_id, first_name, username)


# Универсальная функция обновления полей пользователя
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

# Примеры:
# await update_user_fields(user_id, first_name="Алиса", username="alisa2025", is_active=True)
# await update_user_fields(user_id, eighteen_years_old=True)


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


