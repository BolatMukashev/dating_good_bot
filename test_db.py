import asyncio
from models import User, ReactionType, Gender
import random
from faker import Faker
from sqlalchemy import select
from functions import *
from config import ADMIN_ID
from db_connect import AsyncSessionLocal


fake = Faker("ru_RU")


WOMAN_PHOTO = 'AgACAgIAAxkBAAIEXWhyM6aDeihjOMGDRT4wm2zQlBVnAAJ_AjIbE9uYS_5EbII1p1GkAQADAgADeQADNgQ'
MAN_PHOTO = 'AgACAgIAAxkBAAIEZmhyNMfHJtQKJTEpyBvnzSn78uxBAALc8jEbht2QSwgCthHAoX1JAQADAgADeQADNgQ'


# TODO добавить ANY


async def add_new_fake_user(gender: Gender, tg_id: int, gender_search=True, random_location=False):
    async with AsyncSessionLocal() as session:
        if tg_id == 0:
            tg_id = random.randint(100000000, 999999999)
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

        new_user = User(telegram_id= tg_id,
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
        
async def test():
    # сценарий MATCH
    await add_new_fake_user(Gender.WOMAN, tg_id=1111, gender_search=True, random_location=False)
    await add_reaction(1111, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 1111, ReactionType.LOVE.value)

    # сценарий LOVE
    await add_new_fake_user(Gender.WOMAN, tg_id=2222, gender_search=True, random_location=False)
    await add_reaction(2222, ADMIN_ID, ReactionType.LOVE.value)

    # сценарий SEX
    await add_new_fake_user(Gender.WOMAN, tg_id=3333, gender_search=True, random_location=False)
    await add_reaction(3333, ADMIN_ID, ReactionType.SEX.value)

    # сценарий CHAT
    await add_new_fake_user(Gender.WOMAN, tg_id=4444, gender_search=True, random_location=False)
    await add_reaction(4444, ADMIN_ID, ReactionType.CHAT.value)

    # сценарий SKIP
    await add_new_fake_user(Gender.WOMAN, tg_id=5555, gender_search=True, random_location=False)
    await add_reaction(5555, ADMIN_ID, ReactionType.SKIP.value)

    # сценарий COLLECTION
    await add_new_fake_user(Gender.WOMAN, tg_id=6666, gender_search=True, random_location=False)
    await add_reaction(6666, ADMIN_ID, ReactionType.SEX.value)

    # сценарий SEARCH TRUE
    await add_new_fake_user(Gender.WOMAN, tg_id=7111, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=7112, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=7113, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=7114, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=7115, gender_search=True, random_location=False)

    # сценарий SEARCH FALSE
    await add_new_fake_user(Gender.WOMAN, tg_id=8111, gender_search=False, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=8112, gender_search=True, random_location=True)
    await add_new_fake_user(Gender.MAN, tg_id=8113, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=8114, gender_search=False, random_location=True)
    await add_new_fake_user(Gender.ANY, tg_id=8115, gender_search=True, random_location=False)


async def test2():
    # сценарий SEARCH TRUE
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=True, random_location=False)

    # сценарий SEARCH FALSE
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=False, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=True, random_location=True)
    await add_new_fake_user(Gender.MAN, tg_id=0, gender_search=True, random_location=False)
    await add_new_fake_user(Gender.WOMAN, tg_id=0, gender_search=False, random_location=True)
    await add_new_fake_user(Gender.ANY, tg_id=0, gender_search=True, random_location=False)


async def test3():
    await add_reaction(251093196, ADMIN_ID, ReactionType.SEX.value)


if __name__ == "__main__":
    asyncio.run(test3())

