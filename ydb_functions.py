import asyncio
import ydb
import ydb.aio
from enum import Enum
from typing import Optional, Dict, Any, List
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN, LOCAL_WEBHOOK
from dataclasses import dataclass
from datetime import datetime, timezone


# yc iam create-token   (12 часов действует)
# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту
# пропускная способность базы - 50 запросов/секунду сейчас


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
           'YDBClient'
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
        self.credentials = ydb.AccessTokenCredentials(self.token) if LOCAL_WEBHOOK else ydb.iam.MetadataUrlCredentials()
    
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
            credentials=self.credentials,
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

    async def search_user(self, telegram_id: int, first_name: str, username: str) -> Optional[User]:
        """
        Поиск одного пользователя по критериям и возврат объекта User:
        - 1-й приоритет: страна + город
        - 2-й приоритет: страна
        - если не найдено → None
        - учитываем gender/gender_search (ANY)
        Теперь поиск исключает:

        - Забаненных пользователей
        - C влюченным режимом incognito
        - Пользователей без username
        - Тех, кому уже ставились реакции
        - Тех, кому уже были произведены платежи
        """

        query = f"""
            DECLARE $telegram_id AS Uint64;
            DECLARE $first_name AS Utf8;
            DECLARE $username AS Utf8;

            -- сначала обновляем username и first_name
            UPSERT INTO users (telegram_id, first_name, username)
            VALUES ($telegram_id, $first_name, $username);

            SELECT u2.telegram_id AS found_id
            FROM users AS u1
            INNER JOIN users AS u2
                ON u1.country = u2.country
            INNER JOIN user_settings AS s
                ON u2.telegram_id = s.telegram_id
            LEFT JOIN reactions AS r
                ON r.telegram_id = u1.telegram_id
                AND r.target_tg_id = u2.telegram_id
            LEFT JOIN payments AS p
                ON p.telegram_id = u1.telegram_id
                AND p.target_tg_id = u2.telegram_id
            WHERE u1.telegram_id = $telegram_id
            AND u1.telegram_id != u2.telegram_id
            AND u2.username IS NOT NULL
            AND u2.username != ""
            AND s.banned = false
            AND s.incognito_switch = false
            AND r.telegram_id IS NULL
            AND p.telegram_id IS NULL  -- исключаем тех, кому уже платили
            AND (
                (u1.gender = u2.gender_search OR u2.gender_search = 'ANY')
                AND (u2.gender = u1.gender_search OR u1.gender_search = 'ANY')
            )
            ORDER BY
                CASE WHEN u1.city = u2.city THEN 1 ELSE 2 END,
                u2.telegram_id
            LIMIT 1;
        """

        result_sets = await self.execute_query(
            query,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
             "$first_name": (first_name, ydb.PrimitiveType.Utf8),
            "$username": (username, ydb.PrimitiveType.Utf8)
            },
        )

        found_id = None
        for result_set in result_sets:
            for row in result_set.rows:
                if "found_id" in row:
                    found_id = int(row["found_id"])
                    break  # Нашли первый подходящий ID, выходим из циклов
            if found_id:
                break

        # Если ID найден, используем get_user_by_id для получения полного объекта
        if found_id is not None:
            return await self.get_user_by_id(found_id)

        return None


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
    
    async def find_first_matching_user(self, current_user_id: int) -> Optional[FullUser]:
        """
        Найти первого подходящего пользователя для знакомств используя упрощенную логику
        """
        # По данные текущего пользователя
        current_user = await self.get_full_user_by_id(current_user_id)
        if not current_user:
            return None
        
        # Получаем список исключений (пользователи, на которых уже реагировал)
        reacted_users_query = """
            DECLARE $current_user_id AS Uint64;
            
            SELECT DISTINCT target_tg_id
            FROM reactions
            WHERE telegram_id = $current_user_id;
        """
        
        reacted_result = await self.user_client.execute_query(
            reacted_users_query,
            {"$current_user_id": (current_user_id, ydb.PrimitiveType.Uint64)}
        )
        
        reacted_users = {row["target_tg_id"] for row in reacted_result[0].rows}
        
        # Получаем список пользователей в коллекции (оплаченных)
        collection_users_query = """
            DECLARE $current_user_id AS Uint64;
            
            SELECT DISTINCT target_tg_id
            FROM payments
            WHERE telegram_id = $current_user_id AND target_tg_id IS NOT NULL;
        """
        
        collection_result = await self.user_client.execute_query(
            collection_users_query,
            {"$current_user_id": (current_user_id, ydb.PrimitiveType.Uint64)}
        )
        
        collection_users = {row["target_tg_id"] for row in collection_result[0].rows if row["target_tg_id"]}
        
        # Объединяем исключения
        excluded_users = reacted_users.union(collection_users)
        excluded_users.add(current_user_id)
        
        # Формируем условие исключения для SQL
        if excluded_users:
            excluded_ids_str = ", ".join(str(uid) for uid in excluded_users)
            exclusion_condition = f"AND u.telegram_id NOT IN ({excluded_ids_str})"
        else:
            exclusion_condition = ""
        
        # Формируем условия по полу
        gender_conditions = []
        
        # Кого ты ищешь
        if current_user.gender_search and current_user.gender_search != "ANY":
            gender_conditions.append(f"AND u.gender = '{current_user.gender_search}'")
        
        # Подходишь ли ты им
        if current_user.gender and current_user.gender != "ANY":
            gender_conditions.append(f"AND (u.gender_search = '{current_user.gender}' OR u.gender_search = 'ANY' OR u.gender_search IS NULL)")
        else:
            gender_conditions.append("AND (u.gender_search = 'ANY' OR u.gender_search IS NULL)")
        
        gender_condition = " ".join(gender_conditions)
        
        # Шаг 1: Поиск в том же городе и стране
        if current_user.city and current_user.country:
            city_query = f"""
                SELECT u.telegram_id
                FROM users AS u
                INNER JOIN user_settings AS s ON u.telegram_id = s.telegram_id
                WHERE u.username IS NOT NULL
                    AND u.username != ""
                    AND u.photo_id IS NOT NULL  
                    AND u.photo_id != ""
                    AND u.about_me IS NOT NULL
                    AND u.about_me != ""
                    AND s.incognito_switch = false
                    AND s.banned = false
                    AND u.city = '{current_user.city}'
                    AND u.country = '{current_user.country}'
                    {gender_condition}
                    {exclusion_condition}
                LIMIT 1;
            """
            
            city_result = await self.user_client.execute_query(city_query)
            
            if city_result[0].rows:
                found_user_id = city_result[0].rows[0]["telegram_id"]
                return await self.get_full_user_by_id(found_user_id)

        # Шаг 2: Поиск в той же стране
        if current_user.country:
            country_query = f"""
                SELECT u.telegram_id
                FROM users AS u
                INNER JOIN user_settings AS s ON u.telegram_id = s.telegram_id
                WHERE u.username IS NOT NULL
                    AND u.username != ""
                    AND u.photo_id IS NOT NULL
                    AND u.photo_id != ""  
                    AND u.about_me IS NOT NULL
                    AND u.about_me != ""
                    AND s.incognito_switch = false
                    AND s.banned = false
                    AND u.country = '{current_user.country}'
                    {gender_condition}
                    {exclusion_condition}
                LIMIT 1;
            """
            
            country_result = await self.user_client.execute_query(country_query)
            
            if country_result[0].rows:
                found_user_id = country_result[0].rows[0]["telegram_id"]
                return await self.get_full_user_by_id(found_user_id)

        return None
    
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
                `telegram_id` Uint64 NOT NULL,
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
            DECLARE $telegram_id AS Uint64;
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
            DECLARE $telegram_id AS Uint64;

            SELECT parameter, message_id
            FROM cache
            WHERE telegram_id = $telegram_id
            ORDER BY parameter;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

        rows = result[0].rows
        return {row["parameter"]: row["message_id"] for row in rows}

    async def delete_cache_by_telegram_id(self, telegram_id: int) -> None:
        """
        Удаление всех записей кэша для пользователя
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DELETE FROM cache WHERE telegram_id = $telegram_id;
            """,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)}
        )

    async def delete_cache_by_telegram_id_and_parameter(self, telegram_id: int, parameter: str) -> None:
        """
        Удаление записи кэша по telegram_id и параметру
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $parameter AS Utf8;
            DELETE FROM cache WHERE telegram_id = $telegram_id AND parameter = $parameter;
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
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
            "$telegram_id": (cache.telegram_id, ydb.PrimitiveType.Uint64),
            "$parameter": (cache.parameter, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$message_id": (cache.message_id, ydb.OptionalType(ydb.PrimitiveType.Int32)),
        }


# ------------------------------------------------------------ ПЛАТЕЖИ -----------------------------------------------------------


@dataclass
class Payment:
    telegram_id: int
    amount: int
    payment_type: str
    target_tg_id: Optional[int] = None
    id: Optional[int] = None
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
   
    async def get_collection_targets_with_filter(self, telegram_id: int) -> tuple[list[int], int]:
        """
        как get_collection_targets но исключает из поиска:
        * пользователей без username (NULL или пустая строка)
        * пользователей с banned = true (таблица user_settings)
        """
        query = f"""
            DECLARE $telegram_id AS Uint64;
            
            SELECT p.target_tg_id AS target_id
            FROM payments AS p
            INNER JOIN users AS u
            ON p.target_tg_id = u.telegram_id
            INNER JOIN user_settings AS s
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
    created_at: Optional[int] = None  # Храним как timestamp (секунды с эпохи)


class ReactionClient(YDBClient):
    def __init__(self, endpoint: str = YDB_ENDPOINT, database: str = YDB_PATH, token: str = YDB_TOKEN):
        super().__init__(endpoint, database, token)
        self.table_name = "reactions"
        self.table_schema = """
            CREATE TABLE `reactions` (
                `telegram_id` Uint64 NOT NULL,
                `target_tg_id` Uint64 NOT NULL,
                `reaction` Utf8 NOT NULL,
                `created_at` Uint64 NOT NULL,
                PRIMARY KEY (`telegram_id`, `target_tg_id`, `reaction`),
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
        Вставка или обновление реакции
        Сначала удаляем существующую запись, потом вставляем новую
        """
        if reaction.created_at is None:
            reaction.created_at = int(datetime.now(timezone.utc).timestamp())
        
        # Сначала удаляем существующую реакцию (если есть)
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;
            
            DELETE FROM reactions 
            WHERE telegram_id = $telegram_id 
            AND target_tg_id = $target_tg_id;
            """,
            {
                "$telegram_id": (reaction.telegram_id, ydb.PrimitiveType.Uint64),
                "$target_tg_id": (reaction.target_tg_id, ydb.PrimitiveType.Uint64)
            }
        )
        
        # Затем вставляем новую
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;
            DECLARE $reaction AS Utf8;
            DECLARE $created_at AS Uint64;

            INSERT INTO reactions (telegram_id, target_tg_id, reaction, created_at)
            VALUES ($telegram_id, $target_tg_id, $reaction, $created_at);
            """,
            self._to_params(reaction)
        )
        return reaction

    async def delete_reaction(self, telegram_id: int, target_tg_id: int) -> None:
        """
        Удаление реакции по составному ключу
        """
        await self.execute_query(
            """
            DECLARE $telegram_id AS Uint64;
            DECLARE $target_tg_id AS Uint64;
            
            DELETE FROM reactions 
            WHERE telegram_id = $telegram_id 
            AND target_tg_id = $target_tg_id;
            """,
            {
                "$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64),
                "$target_tg_id": (target_tg_id, ydb.PrimitiveType.Uint64)
            }
        )

    async def get_match_users(self, telegram_id: int) -> tuple[dict[int, str], int]:
        """
        Найти пользователей, которые поставили такую же реакцию, что и наш пользователь им.
        Возвращает словарь: {matched_user_id: reaction}.
        Исключаем:
        - забаненных пользователей
        - пользователей без username
        """
        query = f"""
            DECLARE $telegram_id AS Uint64;

            SELECT DISTINCT 
                r2.telegram_id AS matched_user_id,
                r1.reaction AS reaction
            FROM reactions AS r1
            
            INNER JOIN reactions AS r2
            ON r1.target_tg_id = r2.telegram_id 
            AND r1.telegram_id = r2.target_tg_id
            AND r1.reaction = r2.reaction
            
            INNER JOIN users AS u
            ON r2.telegram_id = u.telegram_id
            
            INNER JOIN user_settings AS s
            ON r2.telegram_id = s.telegram_id
            
            WHERE r1.telegram_id = $telegram_id
            AND u.username IS NOT NULL
            AND u.username != ""
            AND s.banned = false
            AND r1.reaction != "SKIP";
        """

        result_sets = await self.execute_query(
            query,
            {"$telegram_id": (telegram_id, ydb.PrimitiveType.Uint64)},
        )

        matches: dict[int, str] = {}
        for result_set in result_sets:
            for row in result_set.rows:
                if "matched_user_id" in row and "reaction" in row:
                    matches[int(row["matched_user_id"])] = row["reaction"]

        # отсортировать по ключу как в get_match_targets
        matches = dict(sorted(matches.items(), key=lambda x: x[0]))

        return matches, len(matches)

    async def get_intent_targets(self, user_id: int, intent: str) -> tuple[List[int], int]:
        """
        Найти тех, кто поставил МНЕ указанную реакцию,
        исключая:
        - тех, кому Я уже ответил той же реакцией (MATCH)
        - тех, кого Я пропустил (SKIP)
        - тех, кого Я оплатил (запись в payments)
        - забаненных
        - пользователей без username
        """
        query = f"""
            DECLARE $user_id AS Uint64;
            DECLARE $intent AS Utf8;

            SELECT main.telegram_id AS telegram_id,
                main.reaction AS reaction
            FROM (
                SELECT r.telegram_id AS telegram_id,
                    r.reaction AS reaction
                FROM reactions AS r
                INNER JOIN users AS u ON r.telegram_id = u.telegram_id
                INNER JOIN user_settings AS s ON r.telegram_id = s.telegram_id
                WHERE r.target_tg_id = $user_id
                AND r.reaction = $intent
                AND u.username IS NOT NULL
                AND u.username != ""
                AND s.banned = false
            ) AS main
            LEFT JOIN (
                SELECT telegram_id, target_tg_id
                FROM reactions 
                WHERE telegram_id = $user_id AND reaction = $intent
            ) AS mutual
            ON main.telegram_id = mutual.target_tg_id
            LEFT JOIN (
                SELECT target_tg_id
                FROM payments 
                WHERE telegram_id = $user_id
            ) AS paid
            ON main.telegram_id = paid.target_tg_id
            LEFT JOIN (
                SELECT target_tg_id
                FROM reactions 
                WHERE telegram_id = $user_id AND reaction = "SKIP"
            ) AS skipped
            ON main.telegram_id = skipped.target_tg_id
            WHERE mutual.target_tg_id IS NULL
            AND paid.target_tg_id IS NULL
            AND skipped.target_tg_id IS NULL;
            """

        result_sets = await self.execute_query(
            query,
            {
                "$user_id": (user_id, ydb.PrimitiveType.Uint64),
                "$intent": (intent.upper(), ydb.PrimitiveType.Utf8),
            },
        )

        ids: List[int] = []
        for result_set in result_sets:
            for row in result_set.rows:
                if "telegram_id" in row:
                    ids.append(int(row["telegram_id"]))

        sorted_ids = sorted(set(ids))
        return sorted_ids, len(sorted_ids)

    # --- helpers ---
    def _row_to_reaction(self, row) -> Reaction:
        return Reaction(
            telegram_id=row["telegram_id"],
            target_tg_id=row["target_tg_id"],
            reaction=row["reaction"],
            created_at=row["created_at"],
        )

    def _to_params(self, reaction: Reaction) -> dict:
        return {
            "$telegram_id": (reaction.telegram_id, ydb.PrimitiveType.Uint64),
            "$target_tg_id": (reaction.target_tg_id, ydb.PrimitiveType.Uint64),
            "$reaction": (reaction.reaction, ydb.PrimitiveType.Utf8),
            "$created_at": (reaction.created_at, ydb.PrimitiveType.Uint64),
        }
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Конвертация timestamp в datetime объект"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Конвертация datetime в timestamp"""
        return int(dt.timestamp())


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

