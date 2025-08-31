import asyncio
import ydb
import ydb.aio
from enum import Enum
from typing import Optional, Dict, Any, List
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN, ADMIN_ID
from dataclasses import dataclass


__all__ = ['User',
           'UserClient',
           'Cache',
           'CacheClient',
           ]


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту


class YDBClient:
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        """
        Инициализация клиента YDB
        """
        self.endpoint = endpoint
        self.database = database
        self.token = token
        self.driver = None
        self.pool = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def connect(self):
        """
        Создание соединения с YDB и инициализация пула сессий
        """
        if self.driver is not None:
            return  # уже подключены
            
        driver_config = ydb.DriverConfig(
            self.endpoint, 
            self.database, 
            credentials=ydb.AccessTokenCredentials(self.token),
            root_certificates=ydb.load_ydb_root_certificate(),
        )
        
        self.driver = ydb.aio.Driver(driver_config)
        
        try:
            await self.driver.wait(timeout=5)
            self.pool = ydb.aio.QuerySessionPool(self.driver)
            print("Successfully connected to YDB")
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(self.driver.discovery_debug_details())
            await self.driver.stop()
            self.driver = None
            raise
    
    async def close(self):
        """
        Закрытие соединения с YDB
        """
        if self.pool:
            await self.pool.stop()
            self.pool = None
        
        if self.driver:
            await self.driver.stop()
            self.driver = None
            print("YDB connection closed")
    
    def _ensure_connected(self):
        """
        Проверка, что соединение установлено
        """
        if self.driver is None or self.pool is None:
            raise RuntimeError("YDB client is not connected. Call connect() first or use as async context manager.")
    
    async def table_exists(self, table_name: str) -> bool:
        """
        Проверка существования таблицы
        """
        self._ensure_connected()
        try:
            await self.pool.execute_with_retries(f"SELECT 1 FROM `{table_name}` LIMIT 0;")
            return True
        except ydb.GenericError:
            return False
    
    async def create_table(self, table_name: str, schema: str):
        """
        Создание таблицы с заданной схемой (если она не существует)
        """
        self._ensure_connected()
        print(f"\nChecking if table {table_name} exists...")
        try:
            await self.pool.execute_with_retries(schema)
            print(f"Table {table_name} created successfully!")
        except ydb.GenericError as e:
            if "path exist" in str(e):
                print(f"Table {table_name} already exists, skipping creation.")
            else:
                raise e
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None):
        """
        Выполнение произвольного запроса
        """
        self._ensure_connected()
        return await self.pool.execute_with_retries(query, params)


@dataclass
class User:
    telegram_id: int
    first_name: Optional[str] = None
    username: Optional[str] = None
    gender: Optional[str] = None
    gender_search: Optional[str] = None
    country: Optional[str] = None
    country_local: Optional[str] = None
    city: Optional[str] = None
    city_local: Optional[str] = None
    photo_id: Optional[str] = None
    about_me: Optional[str] = None
    eighteen_years_and_approval: Optional[bool] = False
    incognito_pay: Optional[bool] = False
    incognito_switch: Optional[bool] = False
    banned: Optional[bool] = False


class UserClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "users"
        self.table_schema = """
            CREATE TABLE `users` (
                `telegram_id` Int64 NOT NULL,
                `first_name` Utf8,
                `username` Utf8,
                `gender` Utf8,
                `gender_search` Utf8,
                `country` Utf8,
                `country_local` Utf8,
                `city` Utf8,
                `city_local` Utf8,
                `photo_id` Utf8,
                `about_me` Utf8,
                `eighteen_years_and_approval` Bool,
                `incognito_pay` Bool,
                `incognito_switch` Bool,
                `banned` Bool,
                PRIMARY KEY (`telegram_id`)
            )
        """
    
    async def create_users_table(self):
        """
        Создание таблицы users
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_user(self, user: User) -> User:
        """
        Вставка или обновление пользователя (UPSERT) и возврат объекта User
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;
            DECLARE $first_name AS Utf8?;
            DECLARE $username AS Utf8?;
            DECLARE $gender AS Utf8?;
            DECLARE $gender_search AS Utf8?;
            DECLARE $country AS Utf8?;
            DECLARE $country_local AS Utf8?;
            DECLARE $city AS Utf8?;
            DECLARE $city_local AS Utf8?;
            DECLARE $photo_id AS Utf8?;
            DECLARE $about_me AS Utf8?;
            DECLARE $eighteen_years_and_approval AS Bool?;
            DECLARE $incognito_pay AS Bool?;
            DECLARE $incognito_switch AS Bool?;
            DECLARE $banned AS Bool?;

            UPSERT INTO users (
                telegram_id, first_name, username, gender, gender_search,
                country, country_local, city, city_local, photo_id,
                about_me, eighteen_years_and_approval, incognito_pay,
                incognito_switch, banned
            ) VALUES (
                $telegram_id, $first_name, $username, $gender, $gender_search,
                $country, $country_local, $city, $city_local, $photo_id,
                $about_me, $eighteen_years_and_approval, $incognito_pay,
                $incognito_switch, $banned
            );
            """,
            self._to_params(user)
        )
        return await self.get_user_by_id(user.telegram_id)

    async def get_user_by_id(self, telegram_id: int) -> Optional[User]:
        """
        Получение пользователя по telegram_id
        """
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;

            SELECT telegram_id, first_name, username, gender, gender_search,
                   country, country_local, city, city_local, photo_id,
                   about_me, eighteen_years_and_approval, incognito_pay,
                   incognito_switch, banned
            FROM users
            WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Int64)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_user(rows[0])

    async def update_user(self, user: User) -> User:
        """
        Обновление данных пользователя по объекту User
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;
            DECLARE $first_name AS Utf8?;
            DECLARE $username AS Utf8?;
            DECLARE $gender AS Utf8?;
            DECLARE $gender_search AS Utf8?;
            DECLARE $country AS Utf8?;
            DECLARE $country_local AS Utf8?;
            DECLARE $city AS Utf8?;
            DECLARE $city_local AS Utf8?;
            DECLARE $photo_id AS Utf8?;
            DECLARE $about_me AS Utf8?;
            DECLARE $eighteen_years_and_approval AS Bool?;
            DECLARE $incognito_pay AS Bool?;
            DECLARE $incognito_switch AS Bool?;
            DECLARE $banned AS Bool?;

            UPDATE users SET
                first_name = $first_name,
                username = $username,
                gender = $gender,
                gender_search = $gender_search,
                country = $country,
                country_local = $country_local,
                city = $city,
                city_local = $city_local,
                photo_id = $photo_id,
                about_me = $about_me,
                eighteen_years_and_approval = $eighteen_years_and_approval,
                incognito_pay = $incognito_pay,
                incognito_switch = $incognito_switch,
                banned = $banned
            WHERE telegram_id = $telegram_id;
            """,
            self._to_params(user)
        )
        return await self.get_user_by_id(user.telegram_id)
    
    async def update_user_fields(self, user_id: int, **fields: Any) -> bool:
        """
        Обновление выбранных полей пользователя по user_id.
        Возвращает True, если обновления были, иначе False.
        """
        if not fields:
            return False

        # собираем SET-часть динамически
        set_clauses = []
        params = {"$telegram_id": (user_id, ydb.PrimitiveType.Int64)}

        for idx, (field, value) in enumerate(fields.items(), start=1):
            param_name = f"${field}"
            set_clauses.append(f"{field} = {param_name}")

            # подбираем тип под значение (примерно, можно вынести в мапу типов)
            if isinstance(value, bool):
                params[param_name] = (value, ydb.PrimitiveType.Bool)
            elif isinstance(value, int):
                params[param_name] = (value, ydb.PrimitiveType.Int64)
            else:  # строки и None → Utf8?
                params[param_name] = (value, ydb.OptionalType(ydb.PrimitiveType.Utf8))

        set_query = ", ".join(set_clauses)

        query = f"""
            DECLARE $telegram_id AS Int64;
            {"".join([f"DECLARE {p} AS {('Bool' if isinstance(v[1], ydb.PrimitiveType) and v[1] == ydb.PrimitiveType.Bool else 'Utf8?')};\n" for p, v in params.items() if p != "$telegram_id"])}

            UPDATE users
            SET {set_query}
            WHERE telegram_id = $telegram_id;
        """

        await self.execute_query(query, params)
        return True


    async def delete_user(self, telegram_id: int) -> None:
        """
        Удаление пользователя
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;
            DELETE FROM users WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Int64)}
        )

    # --- helpers ---
    def _row_to_user(self, row) -> User:
        return User(
            telegram_id=row["telegram_id"],
            first_name=row.get("first_name"),
            username=row.get("username"),
            gender=row.get("gender"),
            gender_search=row.get("gender_search"),
            country=row.get("country"),
            country_local=row.get("country_local"),
            city=row.get("city"),
            city_local=row.get("city_local"),
            photo_id=row.get("photo_id"),
            about_me=row.get("about_me"),
            eighteen_years_and_approval=row.get("eighteen_years_and_approval"),
            incognito_pay=row.get("incognito_pay"),
            incognito_switch=row.get("incognito_switch"),
            banned=row.get("banned"),
        )

    def _to_params(self, user: User) -> dict:
        return {
            "$telegram_id": (user.telegram_id, ydb.PrimitiveType.Int64),
            "$first_name": (user.first_name, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$username": (user.username, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$gender": (user.gender, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$gender_search": (user.gender_search, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$country": (user.country, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$country_local": (user.country_local, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$city": (user.city, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$city_local": (user.city_local, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$photo_id": (user.photo_id, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$about_me": (user.about_me, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$eighteen_years_and_approval": (user.eighteen_years_and_approval, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$incognito_pay": (user.incognito_pay, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$incognito_switch": (user.incognito_switch, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$banned": (user.banned, ydb.OptionalType(ydb.PrimitiveType.Bool)),
        }


@dataclass
class Cache:
    telegram_id: int = None
    parameter: Optional[str] = None
    message_id: Optional[int] = None


class CacheClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "cache"
        self.table_schema = """
            CREATE TABLE `cache` (
                `telegram_id` Int64 NOT NULL,
                `parameter` Utf8,
                `message_id` Int32,
                PRIMARY KEY (`telegram_id`, `parameter`)
            )
        """
        
    async def create_cache_table(self):
        """
        Создание таблицы cache
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_cache(self, cache: Cache) -> Cache:
        """
        Вставка записи в кэш
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;
            DECLARE $parameter AS Utf8?;
            DECLARE $message_id AS Int32?;

            UPSERT INTO cache (telegram_id, parameter, message_id)
            VALUES ($telegram_id, $parameter, $message_id);
            """,
            self._to_params(cache)
        )

    async def get_cache_by_telegram_id(self, telegram_id: int) -> dict[str, int]:
        """
        Получение всех записей кэша для пользователя в виде словаря:
        {parameter: message_id}
        """
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;

            SELECT parameter, message_id
            FROM cache
            WHERE telegram_id = $telegram_id
            ORDER BY parameter;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Int64)}
        )

        rows = result[0].rows
        return {row["parameter"]: row["message_id"] for row in rows}


    async def delete_cache_by_telegram_id(self, telegram_id: int) -> None:
        """
        Удаление всех записей кэша для пользователя
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;
            DELETE FROM cache WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Int64)}
        )

    async def delete_cache_by_telegram_id_and_parameter(self, telegram_id: int, parameter: str) -> None:
        """
        Удаление записи кэша по telegram_id и параметру
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Int64;
            DECLARE $parameter AS Utf8;
            DELETE FROM cache WHERE telegram_id = $telegram_id AND parameter = $parameter;
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Int64),
                "$parameter": (parameter, ydb.PrimitiveType.Utf8)
            }
        )

    # --- helpers ---
    def _row_to_cache(self, row) -> Cache:
        return Cache(
            telegram_id=row["telegram_id"],
            parameter=row.get("parameter"),
            message_id=row.get("message_id"),
        )

    def _to_params(self, cache: Cache) -> dict:
        return {
            "$telegram_id": (cache.telegram_id, ydb.PrimitiveType.Int64),
            "$parameter": (cache.parameter, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$message_id": (cache.message_id, ydb.OptionalType(ydb.PrimitiveType.Int32)),
        }


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


async def main():
    """
    Демонстрация различных способов использования
    """
    print("=== Cache Client Demo ===")
    await example_user_usage()
    await example_cache_usage()


async def create_tables_on_ydb():
    # Создание всех таблиц в базе
    async with UserClient() as client:
        await client.create_users_table()
        print("Table 'USERS' created successfully!")

    async with CacheClient() as client:
        await client.create_cache_table()
        print("Table 'CACHE' created successfully!")


if __name__ == "__main__":
    asyncio.run(main())