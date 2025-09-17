from ydb_functions import *
from config import *
import asyncio
from ydb_functions import YDBClient
import random
from faker import Faker
from datetime import datetime, timezone


fake = Faker("ru_RU")


async def add_new_fake_user(
    tg_id: int,
    gender: Gender,
    gender_search: Gender,
    random_country: bool = False,
    random_city: bool = False,
    about_me: str = None,
    incognito: bool = False,
    banned: bool = False,
    username: str = 'astana11b'
):

    if tg_id == 0:
        tg_id = random.randint(10000, 99999)

    if gender == Gender.MAN:
        first_name = fake.first_name_male()
        photo_id = Pictures.TEST_MAN_PHOTO.value
    else:
        first_name = fake.first_name_female()
        photo_id = Pictures.TEST_WOMAN_PHOTO.value

    country = "Kazakhstan" if not random_country else fake.country()
    city = "Oral" if not random_city else fake.city()

    # Заполняем dataclass User
    new_user = User(
        telegram_id=tg_id,
        first_name=first_name,
        username=username,
        gender=gender.value,
        gender_search=gender_search.value,
        country=country,
        country_local=country,
        city=city,
        city_local=city,
        about_me=about_me if about_me else fake.sentence(nb_words=6),
        photo_id=photo_id,
    )

    # Заполняем dataclass UserSettings
    new_settings = UserSettings(
        telegram_id=tg_id,
        eighteen_years_and_approval=True,
        incognito_switch=incognito,
        banned=banned,
        created_at=int(datetime.now(timezone.utc).timestamp()),
    )

    # Используем FullUserClient
    async with FullUserClient() as client:
        full_user = await client.insert_full_user(new_user, new_settings)

    print(f"✅ Пользователь {full_user.first_name} успешно добавлен в базу (ID: {tg_id})")
    return full_user


async def reset_database():
    async with YDBClient() as cleaner:
        await cleaner.clear_all_tables()


async def add_reaction(user_id, target_id, reaction_type: str):
    async with ReactionClient() as client:
        reaction1 = Reaction(user_id, target_id, reaction_type)
        await client.insert_reaction(reaction1)


async def add_payment(user_id, amount, payment_type: PaymentType, target_id):
    async with PaymentClient() as client:
        new_payment = Payment(user_id, amount, payment_type, target_id)
        await client.insert_payment(new_payment)


async def mini_test():
    await add_new_fake_user(1111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти ✅")
    await add_reaction(1111, ADMIN_ID, ReactionType.LOVE.value)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 1111)


async def test_match_menu():
    # должно появится по 1 пользователю во вкладках Совпадение, Коллекция, Свидание, Постель, Чат
    # сценарий MATCH
    await add_new_fake_user(1111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH ✅")
    await add_reaction(1111, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 1111, ReactionType.LOVE.value)

    # сценарий COLLECTION
    await add_new_fake_user(ASTANA_ID, Gender.WOMAN, Gender.MAN, about_me = "Ты должен добавить меня в коллекцию ✅")
    await add_reaction(ASTANA_ID, ADMIN_ID, ReactionType.SEX.value)

    # сценарий LOVE
    await add_new_fake_user(3333, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE ✅")
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


async def test_delete_profile():
    # появятся 4 пользователя во вкладках Совпадение, Свидание, Постель, Чат. Нужно их удалить. Они должны исчезнуть из вкладок
    # сценарий SKIP
    await add_new_fake_user(7111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH и удалить ✅")
    await add_reaction(7111, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(ADMIN_ID, 7111, ReactionType.SEX.value)

    await add_new_fake_user(7112, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE и удалить ✅")
    await add_reaction(7112, ADMIN_ID, ReactionType.LOVE.value)

    await add_new_fake_user(7113, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX и удалить ✅")
    await add_reaction(7113, ADMIN_ID, ReactionType.SEX.value)

    await add_new_fake_user(7114, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT и удалить ✅")
    await add_reaction(7114, ADMIN_ID, ReactionType.CHAT.value)


async def test_banned():
    # мэтч
    await add_new_fake_user(8111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH ✅")
    await add_reaction(8111, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 8111, ReactionType.LOVE.value)
    await add_new_fake_user(8112, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_reaction(8112, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 8112, ReactionType.LOVE.value)

    # коллекция
    await add_new_fake_user(8113, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в COLLECTION ✅")
    await add_new_fake_user(8114, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 8113)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 8114)

    # реакции
    await add_new_fake_user(8115, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE ✅")
    await add_new_fake_user(8116, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX ✅")
    await add_new_fake_user(8117, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT ✅")
    await add_reaction(8115, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(8116, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(8117, ADMIN_ID, ReactionType.CHAT.value)

    await add_new_fake_user(8118, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(8119, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_new_fake_user(8120, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", banned = True)
    await add_reaction(8118, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(8119, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(8120, ADMIN_ID, ReactionType.CHAT.value)


async def test_incognito():
    # мэтч
    await add_new_fake_user(9111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH ✅")
    await add_new_fake_user(9112, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH (инкогнито) ✅", incognito=True)
    await add_reaction(9111, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 9111, ReactionType.LOVE.value)
    await add_reaction(9112, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 9112, ReactionType.LOVE.value)

    # коллекция
    await add_new_fake_user(9113, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в COLLECTION ✅")
    await add_new_fake_user(9114, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в COLLECTION (инкогнито) ✅", incognito = True)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 9113)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 9114)


    # реакции
    await add_new_fake_user(9117, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE ✅")
    await add_new_fake_user(9118, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX ✅")
    await add_new_fake_user(9119, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT ✅")
    await add_reaction(9117, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(9118, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(9119, ADMIN_ID, ReactionType.CHAT.value)

    await add_new_fake_user(9120, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE (инкогнито) ✅", incognito = True)
    await add_new_fake_user(9121, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX (инкогнито) ✅", incognito = True)
    await add_new_fake_user(9122, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT (инкогнито) ✅", incognito = True)
    await add_reaction(9120, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(9121, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(9122, ADMIN_ID, ReactionType.CHAT.value)


async def test_not_username():
    # мэтч
    await add_new_fake_user(9123, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в MATCH ✅")
    await add_reaction(9123, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 9123, ReactionType.LOVE.value)
    await add_new_fake_user(9124, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username = None)
    await add_reaction(9124, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(ADMIN_ID, 9124, ReactionType.LOVE.value)

    # коллекция
    await add_new_fake_user(9125, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в COLLECTION ✅")
    await add_new_fake_user(9126, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username = None)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 9125)
    await add_payment(ADMIN_ID, 1, PaymentType.COLLECTION, 9126)

    # реакции
    await add_new_fake_user(9127, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в LOVE ✅")
    await add_new_fake_user(9128, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в SEX ✅")
    await add_new_fake_user(9129, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в CHAT ✅")
    await add_reaction(9127, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(9128, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(9129, ADMIN_ID, ReactionType.CHAT.value)

    await add_new_fake_user(9130, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username = None)
    await add_new_fake_user(9131, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username = None)
    await add_new_fake_user(9132, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username = None)
    await add_reaction(9130, ADMIN_ID, ReactionType.LOVE.value)
    await add_reaction(9131, ADMIN_ID, ReactionType.SEX.value)
    await add_reaction(9132, ADMIN_ID, ReactionType.CHAT.value)


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

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username = None)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌", username = None)
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌", username = None)

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

    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.MAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.WOMAN, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_city=True, about_me = "Ты не должен меня найти ❌")
    await add_new_fake_user(0, Gender.WOMAN, Gender.ANY, random_country=True, random_city=True, about_me = "Ты не должен меня найти ❌")

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


async def test_get_match():
    async with ReactionClient() as client:
        res = await client.get_intent_targets(ADMIN_ID, ReactionType.SEX.value)
        print(res)


"""
Названия Тестов:

reset_database()
mini_test()

test_match_menu()
test_delete_profile()
test_banned()
test_incognito()
test_not_username()

search_test1() - M search W - 4 положительных результатов
search_test2() - M search M - 4 положительных результатов
search_test3() - M search A - 12 положительных результатов

search_test4() - W search M - 4 положительных результатов
search_test5() - W search W - 4 положительных результатов
search_test6() - W search A - 12 положительных результатов

search_test7() - A search M - 2 положительных результатов
search_test8() - A search W - 2 положительных результатов
search_test9() - A search A - 6 положительных результатов
"""


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту
# пропускная способность базы - 50 запросов/секунду сейчас


if __name__ == "__main__":
    # asyncio.run(reset_database())
    asyncio.run(test_match_menu())
