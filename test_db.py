import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import User
import random
from faker import Faker
from sqlalchemy import select, update
from models import Gender
from functions import *
from config import ADMIN_ID


fake = Faker("ru_RU")


# Настройка подключения к базе
async_engine = create_async_engine("sqlite+aiosqlite:///my_database.db")
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

WOMAN_PHOTO = 'AgACAgIAAxkBAAIEXWhyM6aDeihjOMGDRT4wm2zQlBVnAAJ_AjIbE9uYS_5EbII1p1GkAQADAgADeQADNgQ'
MAN_PHOTO = 'AgACAgIAAxkBAAIEZmhyNMfHJtQKJTEpyBvnzSn78uxBAALc8jEbht2QSwgCthHAoX1JAQADAgADeQADNgQ'


async def add_new_fake_user(gender: Gender, gender_search=True, random_location=False):
    async with AsyncSessionLocal() as session:
        if gender == Gender.MAN:
            first_name=fake.first_name_male()
            photo_id = MAN_PHOTO
            if gender_search:
                gender_search = Gender.WOMAN
            else:
                gender_search = Gender.MAN
        else:
            first_name=fake.first_name_female()
            photo_id = WOMAN_PHOTO
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
                        country_local = country,
                        city = city,
                        city_local = city,
                        about_me = fake.sentence(nb_words=6),
                        photo_id = photo_id,
                        eighteen_years_and_approval = True)
        session.add(new_user)
        await session.commit()
        print("✅ Пользователи успешно добавлены в базу")


async def get_user_by_id(user_id):

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=user_id))
        user = result.scalar_one_or_none()
        if user:
            return user



async def test_add(user_id, target_id, reaction):
    await add_reaction(user_id, target_id, reaction)


if __name__ == "__main__":
    user_id = 638002250
    target_id = ADMIN_ID

    asyncio.run(test_add(target_id, user_id, "LOVE"))
    # for el in range(5):
    #     asyncio.run(add_new_fake_user(Gender.WOMAN, gender_search=True, random_location=True))
