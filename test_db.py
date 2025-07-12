import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, User
import random
from faker import Faker
from sqlalchemy import select, update
from models import Gender


fake = Faker("ru_RU")


# Настройка подключения к базе
async_engine = create_async_engine("sqlite+aiosqlite:///my_database.db")
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def add_new_fake_user(gender: Gender, gender_search=True, random_location=False):
    async with AsyncSessionLocal() as session:
        if gender == Gender.MAN:
            first_name=fake.first_name_male()
            if gender_search:
                gender_search = Gender.WOMAN
            else:
                gender_search = Gender.MAN
        else:
            first_name=fake.first_name_female()
            if gender_search:
                gender_search = Gender.MAN
            else:
                gender_search = Gender.WOMAN
        
        if random_location:
            country = fake.country()
            city = fake.city()
        else:
            country = "Kazakhstan"
            city = "Oral"

        new_user = User(telegram_id= random.randint(100000000, 999999999),
                        first_name=first_name,
                        username="astana11b",
                        gender = gender,
                        gender_search = gender_search,
                        country = country,
                        city = city,
                        about_me = fake.sentence(nb_words=6),
                        photo_id = "AgACAgIAAxkBAAIBJ2hWQly3TGgc6wUgWzTCjx70IsUBAAIv8TEbxFq4ShT9pZ0qhTdgAQADAgADeQADNgQ",
                        eighteen_years_old = True)
        session.add(new_user)
        await session.commit()
        print("✅ Пользователи успешно добавлены в базу")


async def get_user_by_id(user_id):

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=user_id))
        user = result.scalar_one_or_none()
        if user:
            return user


if __name__ == "__main__":
    asyncio.run(add_new_fake_user("WOMAN", gender_search=True, random_location=True))
    # user = asyncio.run(get_user_by_id(930353927))
    # if user:
    #     print(f"Найден пользователь: {user}")
    # else:
    #     print("Пользователь не найден")
    
