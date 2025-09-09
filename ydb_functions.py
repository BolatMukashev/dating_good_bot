import asyncio
import ydb
import ydb.aio
from enum import Enum
from typing import Optional, Dict, Any, List, Tuple
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN, ADMIN_ID
from dataclasses import dataclass
from datetime import datetime, timezone


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту


__all__ = ['User',
           'UserClient',
           'UserSettings',
           'UserSettingsClient',
           'FullUser',
           'FullUserClient',
           'Gender',
           'Cache',
           'CacheClient',
           'Payment',
           'PaymentClient',
           'PaymentType',
           'ReactionType',
           'Reaction',
           'ReactionClient',
           'SearchClient'
           ]


# ---------------------------------------------------------- ДОП. УСТАНОВКИ --------------------------------------------------------


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


# ---------------------------------------------------------- БАЗОВЫЙ КЛАСС ---------------------------------------------------------


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


# ------------------------------------------------------------ АНКЕТА -----------------------------------------------------------


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


@dataclass
class UserSettings:
    telegram_id: int
    eighteen_years_and_approval: Optional[bool] = False
    incognito_pay: Optional[bool] = False
    incognito_switch: Optional[bool] = False
    banned: Optional[bool] = False
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)


@dataclass
class FullUser:
    """Объединенные данные пользователя и его настроек"""
    user: User
    settings: UserSettings

    @property
    def telegram_id(self) -> int:
        return self.user.telegram_id
    
    @property
    def first_name(self) -> str:
        return self.user.first_name
    
    @property
    def username(self) -> str:
        return self.user.username
    
    @property
    def gender(self) -> str:
        return self.user.gender

    @property
    def gender_search(self) -> str:
        return self.user.gender_search
    
    @property
    def country(self) -> str | None:
        return self.user.country
    
    @property
    def country_local(self) -> str | None:
        return self.user.country_local

    @property
    def city(self) -> str | None:
        return self.user.city

    @property
    def city_local(self) -> str | None:
        return self.user.city_local

    @property
    def photo_id(self) -> str | None:
        return self.user.photo_id

    @property
    def about_me(self) -> str | None:
        return self.user.about_me
    
    @property
    def eighteen_years_and_approval(self) -> bool:
        return self.settings.eighteen_years_and_approval

    @property
    def incognito_pay(self) -> bool:
        return self.settings.incognito_pay

    @property
    def incognito_switch(self) -> bool:
        return self.settings.incognito_switch
    
    @property
    def banned(self) -> bool:
        return self.settings.banned
    
    @property
    def created_at(self) -> datetime | None:
        if self.settings.created_at is None:
            return None
        return UserSettingsClient.timestamp_to_datetime(self.settings.created_at)


class UserClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "users"
        self.table_schema = """
            CREATE TABLE `users` (
                `telegram_id` Uint64 NOT NULL,
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
                PRIMARY KEY (`telegram_id`)
            )
        """
    
    async def create_users_table(self):
        """Создание таблицы users"""
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_user(self, user: User) -> User:
        """Вставка или обновление пользователя (UPSERT) и возврат объекта User"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
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

            UPSERT INTO users (
                telegram_id, first_name, username, gender, gender_search,
                country, country_local, city, city_local, photo_id, about_me
            ) VALUES (
                $telegram_id, $first_name, $username, $gender, $gender_search,
                $country, $country_local, $city, $city_local, $photo_id, $about_me
            );
            """,
            self._to_params(user)
        )
        return await self.get_user_by_id(user.telegram_id)

    async def get_user_by_id(self, telegram_id: int) -> Optional[User]:
        """Получение пользователя по telegram_id"""
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;

            SELECT telegram_id, first_name, username, gender, gender_search,
                   country, country_local, city, city_local, photo_id, about_me
            FROM users
            WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_user(rows[0])

    async def update_user(self, user: User) -> User:
        """Обновление данных пользователя по объекту User"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
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
                about_me = $about_me
            WHERE telegram_id = $telegram_id;
            """,
            self._to_params(user)
        )
        return await self.get_user_by_id(user.telegram_id)
    
    async def update_user_fields(self, user_id: int, **fields: Any) -> bool:
        """Обновление выбранных полей пользователя по user_id"""
        if not fields:
            return False

        # Фильтруем только поля, которые относятся к таблице users
        user_fields = {k: v for k, v in fields.items() 
                      if k in ['first_name', 'username', 'gender', 'gender_search', 
                              'country', 'country_local', 'city', 'city_local', 
                              'photo_id', 'about_me']}
        
        if not user_fields:
            return False

        set_clauses = []
        params = {"$telegram_id": (user_id, ydb.PrimitiveType.Uint64)}

        for field, value in user_fields.items():
            param_name = f"${field}"
            set_clauses.append(f"{field} = {param_name}")
            params[param_name] = (value, ydb.OptionalType(ydb.PrimitiveType.Utf8))

        set_query = ", ".join(set_clauses)
        declare_params = "\n".join([f"DECLARE {p} AS Utf8?;" for p in params.keys() if p != "$telegram_id"])

        query = f"""
            DECLARE $telegram_id AS Uint64;
            {declare_params}

            UPDATE users
            SET {set_query}
            WHERE telegram_id = $telegram_id;
        """

        await self.execute_query(query, params)
        return True

    async def delete_user(self, telegram_id: int) -> None:
        """Удаление пользователя"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DELETE FROM users WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

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
        )

    def _to_params(self, user: User) -> dict:
        return {
            "$telegram_id": (user.telegram_id, ydb.PrimitiveType.Uint64),
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
        }


class UserSettingsClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "user_settings"
        self.table_schema = """
            CREATE TABLE `user_settings` (
                `telegram_id` Uint64 NOT NULL,
                `eighteen_years_and_approval` Bool,
                `incognito_pay` Bool,
                `incognito_switch` Bool,
                `banned` Bool,
                `created_at` Uint64,
                PRIMARY KEY (`telegram_id`)
            )
        """
    
    async def create_user_settings_table(self):
        """Создание таблицы user_settings"""
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_user_settings(self, settings: UserSettings) -> UserSettings:
        """Вставка или обновление настроек пользователя (UPSERT)"""
        existing_settings = await self.get_user_settings_by_id(settings.telegram_id)
        
        if existing_settings:
            if settings.created_at is None:
                settings.created_at = existing_settings.created_at
        else:
            if settings.created_at is None:
                from datetime import datetime, timezone
                settings.created_at = int(datetime.now(timezone.utc).timestamp())
        
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $eighteen_years_and_approval AS Bool?;
            DECLARE $incognito_pay AS Bool?;
            DECLARE $incognito_switch AS Bool?;
            DECLARE $banned AS Bool?;
            DECLARE $created_at AS Uint64?;

            UPSERT INTO user_settings (
                telegram_id, eighteen_years_and_approval, incognito_pay,
                incognito_switch, banned, created_at
            ) VALUES (
                $telegram_id, $eighteen_years_and_approval, $incognito_pay,
                $incognito_switch, $banned, $created_at
            );
            """,
            self._to_params(settings)
        )
        return await self.get_user_settings_by_id(settings.telegram_id)

    async def get_user_settings_by_id(self, telegram_id: int) -> Optional[UserSettings]:
        """Получение настроек пользователя по telegram_id"""
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;

            SELECT telegram_id, eighteen_years_and_approval, incognito_pay,
                   incognito_switch, banned, created_at
            FROM user_settings
            WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_settings(rows[0])

    async def update_user_settings(self, settings: UserSettings) -> UserSettings:
        """Обновление настроек пользователя"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $eighteen_years_and_approval AS Bool?;
            DECLARE $incognito_pay AS Bool?;
            DECLARE $incognito_switch AS Bool?;
            DECLARE $banned AS Bool?;
            DECLARE $created_at AS Uint64?;

            UPDATE user_settings SET
                eighteen_years_and_approval = $eighteen_years_and_approval,
                incognito_pay = $incognito_pay,
                incognito_switch = $incognito_switch,
                banned = $banned,
                created_at = $created_at
            WHERE telegram_id = $telegram_id;
            """,
            self._to_params(settings)
        )
        return await self.get_user_settings_by_id(settings.telegram_id)
    
    async def create_user_settings(self, settings: UserSettings) -> UserSettings:
        """Создание новых настроек пользователя (только INSERT)"""
        if settings.created_at is None:
            from datetime import datetime, timezone
            settings.created_at = int(datetime.now(timezone.utc).timestamp())
        
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $eighteen_years_and_approval AS Bool?;
            DECLARE $incognito_pay AS Bool?;
            DECLARE $incognito_switch AS Bool?;
            DECLARE $banned AS Bool?;
            DECLARE $created_at AS Uint64;

            INSERT INTO user_settings (
                telegram_id, eighteen_years_and_approval, incognito_pay,
                incognito_switch, banned, created_at
            ) VALUES (
                $telegram_id, $eighteen_years_and_approval, $incognito_pay,
                $incognito_switch, $banned, $created_at
            );
            """,
            {
                "$telegram_id": (settings.telegram_id, ydb.PrimitiveType.Uint64),
                "$eighteen_years_and_approval": (settings.eighteen_years_and_approval, ydb.OptionalType(ydb.PrimitiveType.Bool)),
                "$incognito_pay": (settings.incognito_pay, ydb.OptionalType(ydb.PrimitiveType.Bool)),
                "$incognito_switch": (settings.incognito_switch, ydb.OptionalType(ydb.PrimitiveType.Bool)),
                "$banned": (settings.banned, ydb.OptionalType(ydb.PrimitiveType.Bool)),
                "$created_at": (settings.created_at, ydb.PrimitiveType.Uint64),
            }
        )
        return await self.get_user_settings_by_id(settings.telegram_id)
    
    async def update_user_settings_fields(self, user_id: int, **fields: Any) -> bool:
        """Обновление выбранных полей настроек пользователя"""
        if not fields:
            return False

        settings_fields = {k: v for k, v in fields.items() 
                          if k in ['eighteen_years_and_approval', 'incognito_pay', 
                                  'incognito_switch', 'banned', 'created_at']}
        
        if not settings_fields:
            return False

        set_clauses = []
        params = {"$telegram_id": (user_id, ydb.PrimitiveType.Uint64)}

        for field, value in settings_fields.items():
            param_name = f"${field}"
            set_clauses.append(f"{field} = {param_name}")
            if field == 'created_at':
                params[param_name] = (value, ydb.OptionalType(ydb.PrimitiveType.Uint64))
            else:
                params[param_name] = (value, ydb.OptionalType(ydb.PrimitiveType.Bool))

        set_query = ", ".join(set_clauses)
        declare_params = []
        for p, v in params.items():
            if p != "$telegram_id":
                if p == "$created_at":
                    declare_params.append(f"DECLARE {p} AS Uint64?;")
                else:
                    declare_params.append(f"DECLARE {p} AS Bool?;")
        
        declare_query = "\n".join(declare_params)

        query = f"""
            DECLARE $telegram_id AS Uint64;
            {declare_query}

            UPDATE user_settings
            SET {set_query}
            WHERE telegram_id = $telegram_id;
        """

        await self.execute_query(query, params)
        return True

    async def delete_user_settings(self, telegram_id: int) -> None:
        """Удаление настроек пользователя"""
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DELETE FROM user_settings WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

    def _row_to_settings(self, row) -> UserSettings:
        return UserSettings(
            telegram_id=row["telegram_id"],
            eighteen_years_and_approval=row.get("eighteen_years_and_approval"),
            incognito_pay=row.get("incognito_pay"),
            incognito_switch=row.get("incognito_switch"),
            banned=row.get("banned"),
            created_at=row.get("created_at"),
        )

    def _to_params(self, settings: UserSettings) -> dict:
        return {
            "$telegram_id": (settings.telegram_id, ydb.PrimitiveType.Uint64),
            "$eighteen_years_and_approval": (settings.eighteen_years_and_approval, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$incognito_pay": (settings.incognito_pay, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$incognito_switch": (settings.incognito_switch, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$banned": (settings.banned, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$created_at": (settings.created_at, ydb.OptionalType(ydb.PrimitiveType.Uint64)),
        }
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int):
        from datetime import datetime, timezone
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt) -> int:
        return int(dt.timestamp())


class FullUserClient:
    """Клиент для работы с объединенными данными пользователя и его настроек"""
    
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        self.user_client = UserClient(endpoint, database, token)
        self.settings_client = UserSettingsClient(endpoint, database, token)
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.user_client.connect()
        await self.settings_client.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.user_client.close()
        await self.settings_client.close()
    
    async def create_tables(self):
        """Создание обеих таблиц"""
        await self.user_client.create_users_table()
        await self.settings_client.create_user_settings_table()
    
    async def get_full_user_by_id(self, telegram_id: int) -> Optional[FullUser]:
        """Получение полных данных пользователя (user + settings)"""
        user = await self.user_client.get_user_by_id(telegram_id)
        if not user:
            return None
        
        settings = await self.settings_client.get_user_settings_by_id(telegram_id)
        if not settings:
            # Создаем настройки по умолчанию, если их нет
            settings = UserSettings(telegram_id=telegram_id)
            await self.settings_client.create_user_settings(settings)
        
        return FullUser(user=user, settings=settings)
    
    async def insert_full_user(self, user: User, settings: Optional[UserSettings] = None) -> FullUser:
        """Вставка пользователя и его настроек"""
        if settings is None:
            settings = UserSettings(telegram_id=user.telegram_id)
        
        await self.user_client.insert_user(user)
        await self.settings_client.create_user_settings(settings)
        
        return FullUser(user=user, settings=settings)
    
    async def update_user_data(self, user: User) -> User:
        """Обновление данных пользователя"""
        return await self.user_client.update_user(user)
    
    async def update_user_settings_data(self, settings: UserSettings) -> UserSettings:
        """Обновление настроек пользователя"""
        return await self.settings_client.update_user_settings(settings)
    
    async def update_user_fields(self, user_id: int, **fields: Any) -> bool:
        """Обновление полей пользователя (автоматически определяет, в какую таблицу записывать)"""
        user_updated = await self.user_client.update_user_fields(user_id, **fields)
        settings_updated = await self.settings_client.update_user_settings_fields(user_id, **fields)
        return user_updated or settings_updated
    
    async def delete_full_user(self, telegram_id: int) -> None:
        """Удаление пользователя и его настроек"""
        await self.settings_client.delete_user_settings(telegram_id)
        await self.user_client.delete_user(telegram_id)


# ------------------------------------------------------------ КЭШ -----------------------------------------------------------


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


# ------------------------------------------------------------ ПЛАТЕЖИ -----------------------------------------------------------


@dataclass
class Payment:
    telegram_id: int
    amount: int
    payment_type: str
    id: Optional[int] = None
    target_tg_id: Optional[int] = None
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)


class PaymentClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "payments"
        self.table_schema = """
            CREATE TABLE `payments` (
                `id` Uint64 NOT NULL,
                `telegram_id` Uint64 NOT NULL,
                `target_tg_id` Uint64,
                `amount` Uint32 NOT NULL,
                `type` Utf8 NOT NULL,
                `created_at` Uint64 NOT NULL,
                PRIMARY KEY (`id`)
            )
        """
    
    async def create_payments_table(self):
        """
        Создание таблицы payments
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_payment(self, payment: Payment) -> Payment:
        """
        Вставка нового платежа с автогенерацией ID
        """
        # Генерируем ID как timestamp в микросекундах для уникальности
        if payment.id is None:
            payment.id = int(datetime.now(timezone.utc).timestamp() * 1000000)
        
        if payment.created_at is None:
            payment.created_at = int(datetime.now(timezone.utc).timestamp())
        
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64?;
            DECLARE $amount AS Uint32;
            DECLARE $type AS Utf8;
            DECLARE $created_at AS Uint64;

            INSERT INTO payments (id, telegram_id, target_tg_id, amount, type, created_at)
            VALUES ($id, $telegram_id, $target_tg_id, $amount, $type, $created_at);
            """,
            self._to_params(payment)
        )

    async def get_collection_targets(self, telegram_id: int) -> tuple[list[int], int]:
            query = f"""
                SELECT target_tg_id
                FROM `{self.table_name}`
                WHERE telegram_id = {telegram_id}
                AND target_tg_id IS NOT NULL
            """
            result_sets = await self.execute_query(query)

            targets = []
            for result_set in result_sets:
                for row in result_set.rows:
                    if row.target_tg_id is not None:
                        targets.append(int(row.target_tg_id))

            return sorted(targets), len(targets)
    
    async def get_collection_targets_with_filter(self, telegram_id: int) -> tuple[list[int], int]:
        """
        как get_collection_targets но исключает из поиска:
        * пользователей без username (NULL или пустая строка)
        * пользователей с banned = true (таблица user_settings)
        """
        query = f"""
            DECLARE $telegram_id AS Uint64;

            SELECT p.target_tg_id AS target_id
            FROM `{self.table_name}` AS p
            INNER JOIN `users` AS u
                ON p.target_tg_id = u.telegram_id
            INNER JOIN `user_settings` AS s
                ON p.target_tg_id = s.telegram_id
            WHERE p.telegram_id = $telegram_id
              AND p.target_tg_id IS NOT NULL
              AND u.username IS NOT NULL
              AND u.username != ""
              AND s.banned = false;
        """

        result_sets = await self.execute_query(
            query,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        targets: list[int] = []
        for result_set in result_sets:
            for row in result_set.rows:
                tgt = row["target_id"]
                if tgt is not None:
                    targets.append(int(tgt))

        return sorted(targets), len(targets)


    async def delete_payment(self, payment_id: int) -> None:
        """
        Удаление платежа по ID
        """
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DELETE FROM payments WHERE id = $id;
            """,
            {"$id": (payment_id, ydb.PrimitiveType.Uint64)}
        )

    # --- helpers ---
    def _row_to_payment(self, row) -> Payment:
        return Payment(
            id=row["id"],
            telegram_id=row["telegram_id"],
            target_tg_id=row.get("target_tg_id"),
            amount=row["amount"],
            payment_type=row["type"],
            created_at=row["created_at"],
        )
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Конвертация timestamp в datetime объект"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Конвертация datetime в timestamp"""
        return int(dt.timestamp())

    def _to_params(self, payment: Payment) -> dict:
        return {
            "$id": (payment.id, ydb.PrimitiveType.Uint64),
            "$telegram_id": (payment.telegram_id, ydb.PrimitiveType.Uint64),  # Uint64 вместо Int64
            "$target_tg_id": (payment.target_tg_id, ydb.OptionalType(ydb.PrimitiveType.Uint64)),  # Uint64 вместо Int64
            "$amount": (payment.amount, ydb.PrimitiveType.Uint32),
            "$type": (payment.payment_type, ydb.PrimitiveType.Utf8),
            "$created_at": (payment.created_at, ydb.PrimitiveType.Uint64),
        }


# ------------------------------------------------------------------ Реакции --------------------------------------------------


@dataclass
class Reaction:
    telegram_id: int
    target_tg_id: int
    reaction: str
    id: Optional[int] = None
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)


class ReactionClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "reactions"
        self.table_schema = """
            CREATE TABLE `reactions` (
                `id` Uint64 NOT NULL,
                `telegram_id` Uint64 NOT NULL,
                `target_tg_id` Uint64 NOT NULL,
                `reaction` Utf8 NOT NULL,
                `created_at` Uint64 NOT NULL,
                PRIMARY KEY (`id`),
                INDEX `ix_reactions_telegram_target_reaction` GLOBAL ON (`telegram_id`, `target_tg_id`, `reaction`),
                INDEX `ix_reactions_target_tg_id` GLOBAL ON (`target_tg_id`)
            )
        """
    
    async def create_reactions_table(self):
        """
        Создание таблицы reactions
        """
        await self.create_table(self.table_name, self.table_schema)
    
    async def insert_reaction(self, reaction: Reaction) -> Reaction:
        """
        Вставка новой реакции с автогенерацией ID
        Проверяет уникальность пары telegram_id + target_tg_id
        """
        # Проверяем, существует ли уже реакция между этими пользователями
        existing = await self.get_reaction_between_users(reaction.telegram_id, reaction.target_tg_id)
        if existing:
            # Обновляем существующую реакцию
            existing.reaction = reaction.reaction
            return await self.update_reaction(existing)
        
        # Генерируем ID как timestamp в микросекундах для уникальности
        if reaction.id is None:
            reaction.id = int(datetime.now(timezone.utc).timestamp() * 1000000)
        
        if reaction.created_at is None:
            reaction.created_at = int(datetime.now(timezone.utc).timestamp())
        
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;
            DECLARE $reaction AS Utf8;
            DECLARE $created_at AS Uint64;

            INSERT INTO reactions (id, telegram_id, target_tg_id, reaction, created_at)
            VALUES ($id, $telegram_id, $target_tg_id, $reaction, $created_at);
            """,
            self._to_params(reaction)
        )
        return reaction

    async def get_reaction_by_id(self, reaction_id: int) -> Optional[Reaction]:
        """
        Получение реакции по ID
        """
        result = await self.execute_query(
            """
            DECLARE $id AS Uint64;

            SELECT id, telegram_id, target_tg_id, reaction, created_at
            FROM reactions
            WHERE id = $id;
            """,
            {"$id": (reaction_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_reaction(rows[0])

    async def get_reaction_between_users(self, telegram_id: int, target_tg_id: int) -> Optional[Reaction]:
        """
        Получение реакции между двумя пользователями
        """
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;

            SELECT id, telegram_id, target_tg_id, reaction, created_at
            FROM reactions
            WHERE telegram_id = $telegram_id AND target_tg_id = $target_tg_id;
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
                "$target_tg_id": (target_tg_id, ydb.PrimitiveType.Uint64)
            }
        )

        rows = result[0].rows
        if not rows:
            return None

        return self._row_to_reaction(rows[0])

    async def get_reactions_sent_by_user(self, telegram_id: int, limit: int = 100) -> List[Reaction]:
        """
        Получение всех реакций, отправленных пользователем
        """
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $limit AS Uint64;

            SELECT id, telegram_id, target_tg_id, reaction, created_at
            FROM reactions
            WHERE telegram_id = $telegram_id
            ORDER BY created_at DESC
            LIMIT $limit;
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
                "$limit": (limit, ydb.PrimitiveType.Uint64)
            }
        )

        return [self._row_to_reaction(row) for row in result[0].rows]

    async def get_reactions_received_by_user(self, target_tg_id: int, limit: int = 100) -> List[Reaction]:
        """
        Получение всех реакций, полученных пользователем
        """
        result = await self.execute_query(
            """
            DECLARE $target_tg_id AS Uint64;
            DECLARE $limit AS Uint64;

            SELECT id, telegram_id, target_tg_id, reaction, created_at
            FROM reactions
            WHERE target_tg_id = $target_tg_id
            ORDER BY created_at DESC
            LIMIT $limit;
            """,
            {
                "$target_tg_id": (target_tg_id, ydb.PrimitiveType.Uint64),
                "$limit": (limit, ydb.PrimitiveType.Uint64)
            }
        )

        return [self._row_to_reaction(row) for row in result[0].rows]

    async def get_mutual_reactions(self, telegram_id: int, target_tg_id: int) -> Dict[str, Optional[Reaction]]:
        """
        Получение взаимных реакций между двумя пользователями
        Возвращает словарь: {'sent': Reaction | None, 'received': Reaction | None}
        """
        result = await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;

            SELECT id, telegram_id, target_tg_id, reaction, created_at
            FROM reactions
            WHERE (telegram_id = $telegram_id AND target_tg_id = $target_tg_id)
               OR (telegram_id = $target_tg_id AND target_tg_id = $telegram_id);
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
                "$target_tg_id": (target_tg_id, ydb.PrimitiveType.Uint64)
            }
        )

        reactions = {'sent': None, 'received': None}
        
        for row in result[0].rows:
            reaction = self._row_to_reaction(row)
            if reaction.telegram_id == telegram_id:
                reactions['sent'] = reaction
            else:
                reactions['received'] = reaction

        return reactions

    async def update_reaction(self, reaction: Reaction) -> Reaction:
        """
        Обновление реакции
        """
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;
            DECLARE $reaction AS Utf8;
            DECLARE $created_at AS Uint64;

            UPDATE reactions SET
                telegram_id = $telegram_id,
                target_tg_id = $target_tg_id,
                reaction = $reaction,
                created_at = $created_at
            WHERE id = $id;
            """,
            self._to_params(reaction)
        )
        return await self.get_reaction_by_id(reaction.id)

    async def delete_reaction(self, reaction_id: int) -> None:
        """
        Удаление реакции по ID
        """
        await self.execute_query(
            """
            DECLARE $id AS Uint64;
            DELETE FROM reactions WHERE id = $id;
            """,
            {"$id": (reaction_id, ydb.PrimitiveType.Uint64)}
        )

    async def count_reactions_received_by_user_and_type(self, target_tg_id: int, reaction: str) -> int:
        """
        Подсчет количества реакций определенного типа, полученных пользователем
        """
        result = await self.execute_query(
            """
            DECLARE $target_tg_id AS Uint64;
            DECLARE $reaction AS Utf8;

            SELECT COUNT(*) as count
            FROM reactions
            WHERE target_tg_id = $target_tg_id AND reaction = $reaction;
            """,
            {
                "$target_tg_id": (target_tg_id, ydb.PrimitiveType.Uint64),
                "$reaction": (reaction, ydb.PrimitiveType.Utf8)
            }
        )

        return result[0].rows[0]["count"] if result[0].rows else 0

    # --- helpers ---
    def _row_to_reaction(self, row) -> Reaction:
        return Reaction(
            id=row["id"],
            telegram_id=row["telegram_id"],
            target_tg_id=row["target_tg_id"],
            reaction=row["reaction"],
            created_at=row["created_at"],
        )

    def _to_params(self, reaction: Reaction) -> dict:
        return {
            "$id": (reaction.id, ydb.PrimitiveType.Uint64),
            "$telegram_id": (reaction.telegram_id, ydb.PrimitiveType.Uint64),
            "$target_tg_id": (reaction.target_tg_id, ydb.PrimitiveType.Uint64),
            "$reaction": (reaction.reaction, ydb.PrimitiveType.Utf8),
            "$created_at": (reaction.created_at, ydb.PrimitiveType.Uint64),
        }

    async def get_intent_targets(self, user_id: int, intent: str) -> tuple[List[int], int]:
        """
        Найти тех, кто поставил МНЕ указанную реакцию, 
        исключая: тех кому я уже отвечал той же реакцией, кого пропустил, кого оплатил, забаненных, без никнейма
        """
        try:
            # Получаем пользователей, которым Я поставил такую же реакцию (взаимные - исключаем)
            mutual_users = await self._get_users_i_reacted_to(user_id, intent.upper())
            
            # Получаем пользователей, которых Я пропустил (исключаем)
            skipped_users = await self._get_users_i_skipped(user_id)
            
            # Получаем пользователей, кого Я оплатил (коллекция - исключаем)
            collection_users = await self._get_users_i_paid_for(user_id)
            
            # Объединяем все исключения в один set
            excluded_users = set(mutual_users + skipped_users + collection_users)
            
            # Строим условие исключения
            excluded_condition = ""
            if excluded_users:
                excluded_ids = ", ".join(str(uid) for uid in excluded_users)
                excluded_condition = f"AND r.telegram_id NOT IN ({excluded_ids})"
            
            # Основной запрос: те, кто поставил МНЕ intent, но не в исключениях
            query = f"""
                DECLARE $user_id AS Uint64;
                DECLARE $intent AS Utf8;

                SELECT r.telegram_id AS telegram_id
                FROM reactions AS r
                INNER JOIN users AS u ON r.telegram_id = u.telegram_id
                INNER JOIN user_settings AS s ON r.telegram_id = s.telegram_id
                WHERE r.target_tg_id = $user_id
                    AND r.reaction = $intent
                    AND u.username IS NOT NULL
                    AND u.username != ""
                    AND s.banned = false
                    {excluded_condition}
                ORDER BY r.telegram_id;
            """
            
            result = await self.execute_query(
                query,
                {
                    "$user_id": (user_id, ydb.PrimitiveType.Uint64),
                    "$intent": (intent.upper(), ydb.PrimitiveType.Utf8)
                }
            )
            
            # Проверяем, что результат не пустой
            if not result or not result[0].rows:
                return [], 0
            
            ids = []
            for row in result[0].rows:
                if "telegram_id" in row:
                    ids.append(row["telegram_id"])
            
            sorted_ids = sorted(set(ids))
            return sorted_ids, len(sorted_ids)
            
        except Exception as e:
            print(f"Error in get_intent_targets: {e}")
            return [], 0

    async def _get_users_i_reacted_to(self, user_id: int, intent: str) -> List[int]:
        """
        Получение списка пользователей, которым Я поставил указанную реакцию
        """
        result = await self.execute_query(
            """
            DECLARE $user_id AS Uint64;
            DECLARE $intent AS Utf8;

            SELECT target_tg_id
            FROM reactions
            WHERE telegram_id = $user_id AND reaction = $intent;
            """,
            {
                "$user_id": (user_id, ydb.PrimitiveType.Uint64),
                "$intent": (intent, ydb.PrimitiveType.Utf8)
            }
        )
        
        return [row["target_tg_id"] for row in result[0].rows]

    async def _get_users_i_skipped(self, user_id: int) -> List[int]:
        """
        Получение списка пользователей, которых Я пропустил (поставил SKIP)
        """
        result = await self.execute_query(
            """
            DECLARE $user_id AS Uint64;

            SELECT target_tg_id
            FROM reactions
            WHERE telegram_id = $user_id AND reaction = "SKIP";
            """,
            {"$user_id": (user_id, ydb.PrimitiveType.Uint64)}
        )
        
        return [row["target_tg_id"] for row in result[0].rows]

    async def _get_users_i_paid_for(self, user_id: int) -> List[int]:
        """
        Получение списка пользователей, кого Я оплатил (добавил в коллекцию)
        """
        result = await self.execute_query(
            """
            DECLARE $user_id AS Uint64;

            SELECT target_tg_id
            FROM payments
            WHERE telegram_id = $user_id AND target_tg_id IS NOT NULL;
            """,
            {"$user_id": (user_id, ydb.PrimitiveType.Uint64)}
        )
        
        return [row["target_tg_id"] for row in result[0].rows if row["target_tg_id"]]
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Конвертация timestamp в datetime объект"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Конвертация datetime в timestamp"""
        return int(dt.timestamp())


# --------------------------------------------------------- ПОИСК -------------------------------------------------------


class SearchClient(YDBClient):
    """Клиент для поиска пользователей в YDB"""
    
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
    
    async def find_first_matching_user(self, current_user_id: int) -> Optional[User]:
        """
        Поиск первого подходящего пользователя для знакомств.
        
        Логика поиска:
        1. Сначала ищем по городу и стране
        2. Если не найдено - ищем по стране
        3. Если совсем никого - возвращаем None
        
        Исключения:
        - Сам пользователь
        - Пользователи без username, photo_id, about_me
        - Пользователи в режиме инкогнито или забаненные
        - Пользователи, на которых уже реагировал
        - Пользователи, которых уже оплатил (добавил в коллекцию)
        """
        self._ensure_connected()
        
        # Получаем данные текущего пользователя
        current_user = await self._get_current_user_data(current_user_id)
        if not current_user:
            return None
        
        # Получаем список исключений (пользователи, на которых уже реагировал)
        reacted_users = await self._get_reacted_users(current_user_id)
        
        # Получаем список пользователей в коллекции (оплаченных)
        collection_users = await self._get_collection_users(current_user_id)
        
        # Объединяем исключения
        excluded_users = set(reacted_users + collection_users + [current_user_id])
        
        # Строим базовые условия поиска
        base_conditions = self._build_base_conditions(current_user, excluded_users)
        
        # Шаг 1: Поиск по городу и стране
        if current_user.get('city') and current_user.get('country'):
            city_query = f"""
                {base_conditions}
                AND u.city = $city AND u.country = $country
                LIMIT 1;
            """
            
            result = await self.execute_query(
                city_query,
                self._get_search_params(current_user, excluded_users, 
                                      city=current_user['city'], 
                                      country=current_user['country'])
            )
            
            if result[0].rows:
                return self._row_to_user(result[0].rows[0])
        
        # Шаг 2: Поиск по стране
        if current_user.get('country'):
            country_query = f"""
                {base_conditions}
                AND u.country = $country
                LIMIT 1;
            """
            
            result = await self.execute_query(
                country_query,
                self._get_search_params(current_user, excluded_users, 
                                      country=current_user['country'])
            )
            
            if result[0].rows:
                return self._row_to_user(result[0].rows[0])
        
        # Шаг 3: Поиск без географических ограничений
        global_query = f"""
            {base_conditions}
            LIMIT 1;
        """
        
        result = await self.execute_query(
            global_query,
            self._get_search_params(current_user, excluded_users)
        )
        
        if result[0].rows:
            return self._row_to_user(result[0].rows[0])
        
        return None
    
    async def _get_current_user_data(self, user_id: int) -> Optional[dict]:
        """Получение данных текущего пользователя"""
        result = await self.execute_query(
            """
            DECLARE $user_id AS Int64;
            
            SELECT u.telegram_id, u.gender, u.gender_search, u.country, u.city,
                   s.incognito_switch, s.banned
            FROM users AS u
            INNER JOIN user_settings AS s ON u.telegram_id = s.telegram_id
            WHERE u.telegram_id = $user_id;
            """,
            {"$user_id": (user_id, ydb.PrimitiveType.Int64)}
        )
        
        if not result[0].rows:
            return None
        
        row = result[0].rows[0]
        
        # Отладочный вывод для понимания структуры данных
        print(f"Row keys: {list(row.keys())}")
        print(f"Row data: {dict(row)}")
        
        # Используем безопасный доступ к данным
        try:
            return {
                'telegram_id': row.get('telegram_id') or row.get('u.telegram_id'),
                'gender': row.get('gender') or row.get('u.gender'),
                'gender_search': row.get('gender_search') or row.get('u.gender_search'),
                'country': row.get('country') or row.get('u.country'),
                'city': row.get('city') or row.get('u.city'),
                'incognito_switch': row.get('incognito_switch') or row.get('s.incognito_switch'),
                'banned': row.get('banned') or row.get('s.banned')
            }
        except Exception as e:
            print(f"Error processing row data: {e}")
            return None
    
    async def _get_reacted_users(self, user_id: int) -> List[int]:
        """Получение списка пользователей, на которых уже реагировал"""
        result = await self.execute_query(
            """
            DECLARE $user_id AS Uint64;
            
            SELECT target_tg_id
            FROM reactions
            WHERE telegram_id = $user_id;
            """,
            {"$user_id": (user_id, ydb.PrimitiveType.Uint64)}
        )
        
        return [row['target_tg_id'] for row in result[0].rows]
    
    async def _get_collection_users(self, user_id: int) -> List[int]:
        """Получение списка пользователей в коллекции (оплаченных)"""
        result = await self.execute_query(
            """
            DECLARE $user_id AS Uint64;
            
            SELECT target_tg_id
            FROM payments
            WHERE telegram_id = $user_id AND target_tg_id IS NOT NULL;
            """,
            {"$user_id": (user_id, ydb.PrimitiveType.Uint64)}
        )
        
        return [row['target_tg_id'] for row in result[0].rows if row['target_tg_id']]
    
    def _build_base_conditions(self, current_user: dict, excluded_users: set) -> str:
        """Построение базовых условий поиска"""
        # Формируем условия по полу
        gender_conditions = self._build_gender_conditions(
            current_user.get('gender'), 
            current_user.get('gender_search')
        )
        
        # Формируем список исключенных пользователей
        excluded_condition = ""
        if excluded_users:
            excluded_ids = ", ".join(str(uid) for uid in excluded_users)
            excluded_condition = f"AND u.telegram_id NOT IN ({excluded_ids})"
        
        return f"""
            DECLARE $user_id AS Int64;
            DECLARE $gender AS Utf8?;
            DECLARE $gender_search AS Utf8?;
            DECLARE $country AS Utf8?;
            DECLARE $city AS Utf8?;
            
            SELECT u.telegram_id, u.first_name, u.username, u.gender, u.gender_search,
                   u.country, u.country_local, u.city, u.city_local, u.photo_id, u.about_me
            FROM users AS u
            INNER JOIN user_settings AS s ON u.telegram_id = s.telegram_id
            WHERE u.username IS NOT NULL
                AND u.photo_id IS NOT NULL
                AND u.about_me IS NOT NULL
                AND s.incognito_switch = false
                AND s.banned = false
                {gender_conditions}
                {excluded_condition}
        """
    
    def _build_gender_conditions(self, user_gender: str, user_gender_search: str) -> str:
        """Построение условий по полу"""
        conditions = []
        
        # Кого ты ищешь
        if user_gender_search == Gender.ANY:
            # Ищешь любого - никаких ограничений по полу кандидатов
            pass
        else:
            # Ищешь конкретный пол
            conditions.append(f"AND u.gender = '{user_gender_search}'")
        
        # Подходишь ли ты им
        if user_gender == Gender.ANY:
            # Ты любого пола - подходишь только тем, кто ищет любого
            conditions.append("AND u.gender_search = 'ANY'")
        else:
            # Ты конкретного пола - подходишь тем, кто ищет твой пол или любого
            conditions.append(f"AND (u.gender_search = '{user_gender}' OR u.gender_search = 'ANY')")
        
        return " ".join(conditions)
    
    def _get_search_params(self, current_user: dict, excluded_users: set, 
                          country: str = None, city: str = None) -> dict:
        """Формирование параметров для запроса"""
        params = {}
        
        if country:
            params["$country"] = (country, ydb.PrimitiveType.Utf8)
        
        if city:
            params["$city"] = (city, ydb.PrimitiveType.Utf8)
        
        return params
    
    def _row_to_user(self, row) -> User:
        """Конвертация строки результата в объект User"""
        return User(
            telegram_id=row.get("u.telegram_id") or row.get("telegram_id"),
            first_name=row.get("u.first_name") or row.get("first_name"),
            username=row.get("u.username") or row.get("username"),
            gender=row.get("u.gender") or row.get("gender"),
            gender_search=row.get("u.gender_search") or row.get("gender_search"),
            country=row.get("u.country") or row.get("country"),
            country_local=row.get("u.country_local") or row.get("country_local"),
            city=row.get("u.city") or row.get("city"),
            city_local=row.get("u.city_local") or row.get("city_local"),
            photo_id=row.get("u.photo_id") or row.get("photo_id"),
            about_me=row.get("u.about_me") or row.get("about_me"),
        )


# --------------------------------------------------------- СОЗДАНИЕ ТАБЛИЦ -------------------------------------------------------


async def create_tables_on_ydb():
    # Создание всех таблиц в базе
    async with UserClient() as client:
        await client.create_users_table()
        print("Table 'USERS' created successfully!")

    async with UserSettingsClient() as client:
        await client.create_user_settings_table()
        print("Table 'USER_SETTINGS' created successfully!")

    async with CacheClient() as client:
        await client.create_cache_table()
        print("Table 'CACHE' created successfully!")

    async with PaymentClient() as client:
        await client.create_payments_table()
        print("Table 'PAYMENTS' created successfully!")

    async with ReactionClient() as client:
        await client.create_reactions_table()
        print("Table 'REACTIONS' created successfully!")


# --------------------------------------------------------- ЗАПУСК -------------------------------------------------------


if __name__ == "__main__":
    asyncio.run(create_tables_on_ydb())

