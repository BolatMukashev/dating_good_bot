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
    gender: str,
    gender_search: str,
    random_country: bool = False,
    random_city: bool = False,
    about_me: str = None,
    incognito: bool = False,
    banned: bool = False,
    username: str = 'astana11b'
):

    if tg_id == 0:
        tg_id = random.randint(10000, 99999)

    if gender == "man":
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
        gender=gender,
        gender_search=gender_search,
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



async def example_user_usage():
    """
    Пример использования с async context manager (рекомендуемый способ)
    """
    async with UserClient() as client:
        # Создание нового пользователя
        # new_user = User(telegram_id=ADMIN_ID, first_name="Alex", username="alex123")
        # await client.insert_user(new_user)
        # print(f"Created user: {user.username}")

        print(await client.get_user_by_id(ADMIN_ID))
        

        # Получение пользователя
        # user = await client.get_user_by_id(ADMIN_ID)
        # if user:
        #     print(f"Found user: {user}")

        # # Обновление пользователя
        # user.incognito_pay = True
        # user.about_me = "Люблю Python 🐍"
        # updated = await client.update_user(user)
        # print(f"Updated user: {updated.first_name}, incognito: {updated.incognito_pay}")

        # await client.update_user_fields(123, banned = True)


async def example_cache_usage():
    """
    Пример использования CacheClient
    """
    async with CacheClient() as cache_client:
        # Создание новой записи кэша
        # new_cache = Cache(telegram_id=123, parameter="test", message_id=123)
        # await cache_client.insert_cache(new_cache)

        # # Получение всех записей для пользователя и итерация по ним
        # user_caches = await cache_client.get_cache_by_telegram_id(123)
        # user_state =  user_caches.get("user_state")
        # print(user_state)

        await cache_client.delete_cache_by_telegram_id(ADMIN_ID)


async def example_payment_usage():
    """
    Пример использования PaymentClient
    """
    async with PaymentClient() as client:
        # Создание таблицы
        await client.create_payments_table()
        
        # Создание нового платежа
        new_payment = Payment(
            telegram_id=ADMIN_ID,
            amount=1000,
            payment_type=PaymentType.COLLECTION.value,
            target_tg_id=None  # для подписки target_tg_id может быть None
        )
        
        payment = await client.insert_payment(new_payment)
        print(f"Created payment: {payment.id}, amount: {payment.amount}")
        
        # Конвертация timestamp в datetime для отображения
        if payment.created_at:
            created_dt = PaymentClient.timestamp_to_datetime(payment.created_at)
            print(f"Payment created at: {created_dt}")
        
        # Получение платежей пользователя
        user_payments = await client.get_payments_by_user(ADMIN_ID)
        print(f"User has {len(user_payments)} payments")


# Пример использования:
async def example_user_settings_usage():
    async with FullUserClient() as client:
        # Создание таблиц
        await client.create_tables()
        
        # Создание пользователя
        user = User(
            telegram_id=123456,
            first_name="John",
            username="john_doe",
        )
        
        settings = UserSettings(
            telegram_id=123456
        )
        
        # Вставка полного пользователя
        full_user = await client.insert_full_user(user, settings)
        
        # Или создание настроек отдельно
        # await client.settings_client.create_user_settings(settings)
        
        # Получение полного пользователя
        retrieved_user = await client.get_full_user_by_id(123456)
        
        # Обновление отдельных полей
        # await client.update_user_fields(123456, first_name="Jane", banned=True)


class YDBCleaner(YDBClient):
    async def clear_all_tables(self):
        """Удаляет все записи во всех таблицах"""
        self._ensure_connected()

        tables = [
            "users",
            "user_settings",
            "payments",
            "cache",
            "reactions"
        ]

        for table in tables:
            try:
                await self.execute_query(f"DELETE FROM `{table}`;")
                print(f"Таблица {table} очищена.")
            except Exception as e:
                print(f"Ошибка при очистке {table}: {e}")


async def example_reaction_usage(target_tg_id: int, reaction_type: ReactionType):
    async with ReactionClient() as client:
        users, count = await client.get_intent_targets(target_tg_id, reaction_type)
        # users, count = await client.get_match_users(target_tg_id)
        print(users, count)


async def reset_database():
    async with YDBCleaner() as cleaner:
        await cleaner.clear_all_tables()


async def test():
    async with UserSettingsClient() as client:
        await client.update_user_settings_fields(5555, banned=True)


async def user_add_test():
    await add_new_fake_user(1111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в Metch ✅")
    await add_new_fake_user(2222, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в Metch ✅")

    await add_new_fake_user(3333, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти в Collections ✅")
    await add_new_fake_user(4444, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти в Collections ❌")

    await add_new_fake_user(5555, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти LOVE ✅")
    await add_new_fake_user(6666, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти SEX ✅")
    await add_new_fake_user(7777, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти CHAT ✅")

    await add_new_fake_user(8888, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти SKIP ❌")
    await add_new_fake_user(9999, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти BAN ❌")
    await add_new_fake_user(9898, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти нет Username ❌")


    async with ReactionClient() as client:
        reaction1 = Reaction(1111, ADMIN_ID, ReactionType.LOVE.value)
        reaction2 = Reaction(2222, ADMIN_ID, ReactionType.LOVE.value)

        reaction3 = Reaction(ADMIN_ID, 1111, ReactionType.LOVE.value)
        reaction4 = Reaction(ADMIN_ID, 2222, ReactionType.LOVE.value)

        reaction5 = Reaction(3333, ADMIN_ID, ReactionType.LOVE.value)
        reaction6 = Reaction(4444, ADMIN_ID, ReactionType.LOVE.value)
        
        await client.insert_reaction(reaction1)
        await client.insert_reaction(reaction2)
        await client.insert_reaction(reaction3)
        await client.insert_reaction(reaction4)
        await client.insert_reaction(reaction5)
        await client.insert_reaction(reaction6)

        reaction7 = Reaction(5555, ADMIN_ID, ReactionType.LOVE.value)
        reaction8 = Reaction(6666, ADMIN_ID, ReactionType.SEX.value)
        reaction9 = Reaction(7777, ADMIN_ID, ReactionType.CHAT.value)

        await client.insert_reaction(reaction7)
        await client.insert_reaction(reaction8)
        await client.insert_reaction(reaction9)

        reaction10 = Reaction(8888, ADMIN_ID, ReactionType.SKIP.value)
        reaction11 = Reaction(ADMIN_ID, 8888, ReactionType.SEX.value)

        await client.insert_reaction(reaction10)
        await client.insert_reaction(reaction11)

        reaction12 = Reaction(9999, ADMIN_ID, ReactionType.SEX.value)
        reaction13 = Reaction(9898, ADMIN_ID, ReactionType.SEX.value)

        await client.insert_reaction(reaction12)
        await client.insert_reaction(reaction13)

    async with PaymentClient() as client:
        payment1 = Payment(telegram_id=ADMIN_ID, amount=10, payment_type=PaymentType.COLLECTION.value, target_tg_id=3333)
        payment2 = Payment(telegram_id=ADMIN_ID, amount=10, payment_type=PaymentType.COLLECTION.value, target_tg_id=4444)

        await client.insert_payment(payment1)
        await client.insert_payment(payment2)
    
    async with UserClient() as client, UserSettingsClient() as settings_client:
        await client.update_user_fields(4444, username=None)
        await client.update_user_fields(9898, username=None)
        await settings_client.update_user_settings_fields(9999, banned=True)


async def search_test(user_id):
    # await add_new_fake_user(1111, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти ✅")
    # await add_new_fake_user(2222, Gender.WOMAN, Gender.ANY, about_me = "Ты должен меня найти ✅")
    # await add_new_fake_user(3333, Gender.WOMAN, Gender.MAN, about_me = "Ты должен меня найти, но не сразу ✅", random_city=True)
    # await add_new_fake_user(4444, Gender.MAN, Gender.WOMAN, about_me = "Ты не должен меня найти ❌")
    # await add_new_fake_user(5555, Gender.MAN, Gender.MAN, about_me = "Ты не должен меня найти ❌")
    # await add_new_fake_user(6666, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", username=None)
    # await add_new_fake_user(7777, Gender.WOMAN, Gender.MAN, about_me = "Ты не должен меня найти ❌", random_country=True)

    await reactiontest(ADMIN_ID, 3333, ReactionType.SKIP.value)

    async with ReactionClient() as client:
        res = await client.search_user(user_id)
        print(res)


async def payment_test2():
    async with PaymentClient() as client:
        res = await client.get_collection_targets_with_filter(ADMIN_ID)
        print(f"Final result: {res}")


async def testtest():
    async with UserClient() as client, UserSettingsClient() as settings_client:
        await client.update_user_fields(2222, username="sadas")


async def reactiontest(user_id, target_id, reaction_type: ReactionType):
    async with ReactionClient() as client:
        reaction1 = Reaction(user_id, target_id, reaction_type)
        # reaction1 = Reaction(ADMIN_ID, 1111, ReactionType.LOVE.value)
        await client.insert_reaction(reaction1)


if __name__ == "__main__":
    # asyncio.run(reset_database())
    # asyncio.run(reactiontest(ADMIN_ID, 3333, ReactionType.LOVE.value))
    asyncio.run(search_test(ADMIN_ID))
    # asyncio.run(example_reaction_usage(ADMIN_ID, ReactionType.LOVE.value))

