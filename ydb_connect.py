import ydb
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN
from enum import Enum
from dataclasses import dataclass, asdict
import os


# yc iam create-token   (12 часов действует)


class PaymentType(str, Enum):
    INCOGNITO = "incognito"
    COLLECTION = "collection"


class Gender(str, Enum):
    MAN = "MAN"
    WOMAN = "WOMAN"
    ANY = "ANY"


# виды реакций
class ReactionType(str, Enum):
    LOVE = "LOVE"
    SEX = "SEX"
    CHAT = "CHAT"
    SKIP = "SKIP"


# -------------------------------------------------------------------

def ydb_test_connect():
    print(f"Endpoint: {YDB_ENDPOINT}")
    print(f"Database: {YDB_PATH}")
    print(f"Token установлен: {'Да' if YDB_TOKEN else 'Нет'}")
    print(f"Длина токена: {len(YDB_TOKEN) if YDB_TOKEN else 0}")

    try:
        driver = ydb.Driver(
            endpoint=YDB_ENDPOINT,
            database=YDB_PATH,
            credentials=ydb.AccessTokenCredentials(YDB_TOKEN) 
        )
        # credentials = ydb.iam.MetadataUrlCredentials() - когда в облаке
        driver.wait(fail_fast=True, timeout=30)
        print("✅ Соединение установлено!")
        driver.stop()
    except Exception as e:
        print(f"❌ Ошибка: {e}")


# -------------------------------------------------------------------


class YDBConnection:
    """Класс для управления подключением к YDB"""

    def __init__(self, endpoint=None, database=None, token=None):
        # Берем параметры либо из аргументов, либо из env
        self.endpoint = YDB_ENDPOINT or os.getenv('YDB_ENDPOINT')
        self.database = YDB_PATH or os.getenv('YDB_PATH')
        self.token = YDB_TOKEN or os.getenv('YDB_TOKEN')
        self._driver = None
        self._pool = None

    def connect(self):
        """Создание подключения и пула сессий"""
        driver_config = ydb.DriverConfig(
            endpoint=self.endpoint,
            database=self.database,
            credentials=ydb.AccessTokenCredentials(self.token)
        )
        self._driver = ydb.Driver(driver_config)
        self._driver.wait(fail_fast=True, timeout=30)
        self._pool = ydb.SessionPool(self._driver)
        return self._pool

    def disconnect(self):
        """Закрытие подключения"""
        if self._driver:
            self._driver.stop()

    @property
    def pool(self):
        """Ленивая инициализация пула"""
        if not self._pool:
            self.connect()
        return self._pool


    def create_users_table(self):
        """Создание таблицы users (если ещё не создана)"""
        def _create_table(session):
            query = """
            CREATE TABLE users (
                telegram_id Int64 NOT NULL,
                first_name Utf8,
                username Utf8,
                gender Utf8,
                gender_search Utf8,
                country Utf8,
                country_local Utf8,
                city Utf8,
                city_local Utf8,
                photo_id Utf8,
                about_me Utf8,
                eighteen_years_and_approval Bool,
                incognito_pay Bool,
                incognito_switch Bool,
                banned Bool,
                PRIMARY KEY (telegram_id)
            )
            """
            session.execute_scheme(query)

        try:
            self.pool.retry_operation_sync(_create_table)
            print("Таблица 'users' успешно создана")
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")


if __name__ == "__main__":
    # только 1 раз, при создании
    conn = YDBConnection()
    conn.create_users_table()
