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


async def add_new_fake_user(tg_id: int, gender: Gender, gender_search: Gender, random_country: bool = False, random_city: bool = False, about_me: str = None, incognito: bool = False, banned: bool = False):
    async with AsyncSessionLocal() as session:
        if tg_id == 0:
            tg_id = random.randint(10000, 99999)
        if gender == Gender.MAN:
            first_name=fake.first_name_male()
            photo_id = MAN_PHOTO
        else:
            first_name=fake.first_name_female()
            photo_id = WOMAN_PHOTO

        country = "Kazakhstan" if not random_country else fake.country()
        city = "Oral" if not random_city else fake.city()
        
        new_user = User(telegram_id= tg_id,
                        first_name=first_name,
                        username="astana11b",
                        gender = gender,
                        gender_search = gender_search,
                        country = country,
                        country_local = country,
                        city = city,
                        city_local = city,
                        about_me = about_me if about_me else fake.sentence(nb_words=6),
                        photo_id = photo_id,
                        eighteen_years_and_approval = True,
                        incognito_switch = incognito,
                        banned = banned)
        session.add(new_user)
        await session.commit()
        print("✅ Пользователи успешно добавлены в базу")


async def get_user_by_id(user_id):

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(telegram_id=user_id))
        user = result.scalar_one_or_none()
        if user:
            return user
        

async def test_match_menu():
    # должно появится по 1 пользователю во вкладках Совпадение, Коллекция, Свидание, Постель, Чат
    # сценарий MATCH
    await add_new_fake_user(1111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH ✅")
    await add_reaction(1111, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 1111, ReactionType.LOVE.value)

    # сценарий COLLECTION
    await add_new_fake_user(2222, Gender.WOMAN, Gender.MAN, about_me = "Ты должен добавить меня в коллекцию ✅")
    await add_reaction(2222, ADMIN_ID, ReactionType.SEX.value)

    # сценарий LOVE
    await add_new_fake_user(3333, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE✅")
    await add_reaction(3333, ADMIN_ID, ReactionType.LOVE.value)

    # сценарий SEX
    await add_new_fake_user(4444, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX ✅")
    await add_reaction(4444, ADMIN_ID, ReactionType.SEX.value)

    # сценарий CHAT
    await add_new_fake_user(5555, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT ✅")
    await add_reaction(5555, ADMIN_ID, ReactionType.CHAT.value)

    # сценарий SKIP
    await add_new_fake_user(6666, Gender.WOMAN, Gender.MAN, about_me = "Ты найдешь меня в поиске, но я уже поставил SKIP ❌")
    await add_reaction(6666, ADMIN_ID, ReactionType.SKIP.value)


async def test_delete_user_from_search():
    # появятся 4 пользователя во вкладках Совпадение, Свидание, Постель, Чат. Нужно их удалить. Они должны исчезнуть из вкладок
    # сценарий SKIP
    await add_new_fake_user(7111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH и удалить✅")
    await add_reaction(7111, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(ADMIN_ID, 7111, ReactionType.SEX.value)

    await add_new_fake_user(7112, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE и удалить✅")
    await add_reaction(7112, ADMIN_ID, ReactionType.LOVE.value)

    await add_new_fake_user(7113, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX и удалить✅")
    await add_reaction(7113, ADMIN_ID, ReactionType.SEX.value)

    await add_new_fake_user(7114, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT и удалить✅")
    await add_reaction(7114, ADMIN_ID, ReactionType.CHAT.value)


async def search_test1():
    # M ищет W
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test2():
    # М ищет М
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test3():
    # М ищет A
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test4():
    # W ищет M
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test5():
    # W ищет W
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test6():
    # W ищет A
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test7():
    # A ищет M
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test8():
    # A ищет W
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


async def search_test9():
    # A ищет A
    # сценарий SEARCH TRUE
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты должен меня найти ✅")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_city=True, about_me = "Ты должен меня найти ✅")

    # сценарий SEARCH FALSE
    await add_new_fake_user(0, Gender.MAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌", incognito = True)

    await add_new_fake_user(0, Gender.MAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(0, Gender.ANY, Gender.ANY, about_me = "Ты не должен меня найти ❌", banned = True)

    await add_new_fake_user(0, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.MAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")


if __name__ == "__main__":
    asyncio.run(search_test1())

