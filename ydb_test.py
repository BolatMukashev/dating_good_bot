from ydb_functions import *
from config import *
import asyncio


async def example_user_usage():
    """
    Пример использования с async context manager (рекомендуемый способ)
    """
    async with UserClient() as client:
        # Создание нового пользователя
        # new_user = User(telegram_id=ADMIN_ID, first_name="Alex", username="alex123")
        # await client.insert_user(new_user)
        # print(f"Created user: {user.username}")

        await client.delete_user(ADMIN_ID)

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


async def main():
    """
    Демонстрация различных способов использования
    """
    print("=== Cache Client Demo ===")
    await example_user_usage()
    await example_cache_usage()


if __name__ == "__main__":
    asyncio.run(example_payment_usage())

