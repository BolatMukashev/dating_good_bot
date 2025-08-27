import asyncio
import ydb
import ydb.aio
from typing import Optional
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN


async def create_connection(endpoint: str, database: str, token: str):
    """
    Создание соединения с YDB
    """
    driver_config = ydb.DriverConfig(
        endpoint, 
        database, 
        credentials=ydb.AccessTokenCredentials(token),
        root_certificates=ydb.load_ydb_root_certificate(),
    )
    
    driver = ydb.aio.Driver(driver_config)
    
    try:
        await driver.wait(timeout=5)
        print("Successfully connected to YDB")
        return driver
    except TimeoutError:
        print("Connect failed to YDB")
        print("Last reported errors by discovery:")
        print(driver.discovery_debug_details())
        await driver.stop()
        raise


async def drop_users_table(pool: ydb.aio.QuerySessionPool):
    """
    Удаление таблицы users (осторожно - удаляет все данные!)
    """
    print("\nDropping table users...")
    try:
        await pool.execute_with_retries("DROP TABLE `users`;")
        print("Table users dropped successfully!")
    except ydb.GenericError as e:
        if "path not exist" in str(e) or "Path does not exist" in str(e):
            print("Table users does not exist, nothing to drop.")
        else:
            raise e


async def table_exists(pool: ydb.aio.QuerySessionPool, table_name: str) -> bool:
    """
    Проверка существования таблицы
    """
    try:
        await pool.execute_with_retries(f"SELECT 1 FROM `{table_name}` LIMIT 0;")
        return True
    except ydb.GenericError:
        return False


async def create_users_table(pool: ydb.aio.QuerySessionPool):
    """
    Создание таблицы users (если она не существует)
    """
    print("\nChecking if table users exists...")
    try:
        await pool.execute_with_retries(
            """
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
        )
        print("Table users created successfully!")
    except ydb.GenericError as e:
        if "path exist" in str(e):
            print("Table users already exists, skipping creation.")
        else:
            raise e


async def insert_user(pool: ydb.aio.QuerySessionPool, 
                      telegram_id: int,
                      first_name: Optional[str] = None,
                      username: Optional[str] = None,
                      gender: Optional[str] = None,
                      gender_search: Optional[str] = None,
                      country: Optional[str] = None,
                      country_local: Optional[str] = None,
                      city: Optional[str] = None,
                      city_local: Optional[str] = None,
                      photo_id: Optional[str] = None,
                      about_me: Optional[str] = None,
                      eighteen_years_and_approval: Optional[bool] = None,
                      incognito_pay: Optional[bool] = None,
                      incognito_switch: Optional[bool] = None,
                      banned: Optional[bool] = False):
    """
    Добавление нового пользователя в таблицу
    """
    print(f"\nInserting user with telegram_id: {telegram_id}")
    
    await pool.execute_with_retries(
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
        {
            "$telegram_id": (telegram_id, ydb.PrimitiveType.Int64),
            "$first_name": (first_name, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$username": (username, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$gender": (gender, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$gender_search": (gender_search, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$country": (country, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$country_local": (country_local, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$city": (city, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$city_local": (city_local, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$photo_id": (photo_id, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$about_me": (about_me, ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            "$eighteen_years_and_approval": (eighteen_years_and_approval, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$incognito_pay": (incognito_pay, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$incognito_switch": (incognito_switch, ydb.OptionalType(ydb.PrimitiveType.Bool)),
            "$banned": (banned, ydb.OptionalType(ydb.PrimitiveType.Bool)),
        }
    )
    print("User inserted successfully!")


async def get_user_by_telegram_id(pool: ydb.aio.QuerySessionPool, telegram_id: int):
    """
    Получение пользователя по telegram_id
    """
    print(f"\nGetting user with telegram_id: {telegram_id}")
    
    result_sets = await pool.execute_with_retries(
        """
        DECLARE $telegram_id AS Int64;

        SELECT 
            telegram_id, first_name, username, gender, gender_search,
            country, country_local, city, city_local, photo_id,
            about_me, eighteen_years_and_approval, incognito_pay,
            incognito_switch, banned
        FROM users 
        WHERE telegram_id = $telegram_id;
        """,
        {
            "$telegram_id": (telegram_id, ydb.PrimitiveType.Int64),
        }
    )
    
    first_set = result_sets[0]
    if first_set.rows:
        for row in first_set.rows:
            print(f"User found: telegram_id={row.telegram_id}, "
                  f"first_name={row.first_name}, username={row.username}")
            return row
    else:
        print("User not found")
        return None


async def update_user(pool: ydb.aio.QuerySessionPool,
                     telegram_id: int,
                     **kwargs):
    """
    Обновление данных пользователя
    """
    print(f"\nUpdating user with telegram_id: {telegram_id}")
    
    # Построение динамического запроса на основе переданных параметров
    set_clauses = []
    parameters = {"$telegram_id": (telegram_id, ydb.PrimitiveType.Int64)}
    declarations = ["DECLARE $telegram_id AS Int64;"]
    
    for key, value in kwargs.items():
        if value is not None:
            param_name = f"${key}"
            set_clauses.append(f"{key} = {param_name}")
            
            # Определение типа для параметра и декларации
            if isinstance(value, bool):
                parameters[param_name] = (value, ydb.PrimitiveType.Bool)
                declarations.append(f"DECLARE {param_name} AS Bool;")
            elif isinstance(value, int):
                parameters[param_name] = (value, ydb.PrimitiveType.Int64)
                declarations.append(f"DECLARE {param_name} AS Int64;")
            else:
                parameters[param_name] = (value, ydb.PrimitiveType.Utf8)
                declarations.append(f"DECLARE {param_name} AS Utf8;")
    
    if not set_clauses:
        print("No parameters to update")
        return
    
    query = f"""
    {' '.join(declarations)}
    
    UPDATE users 
    SET {', '.join(set_clauses)}
    WHERE telegram_id = $telegram_id;
    """
    
    await pool.execute_with_retries(query, parameters)
    print("User updated successfully!")


async def delete_user(pool: ydb.aio.QuerySessionPool, telegram_id: int):
    """
    Удаление пользователя по telegram_id
    """
    print(f"\nDeleting user with telegram_id: {telegram_id}")
    
    await pool.execute_with_retries(
        """
        DECLARE $telegram_id AS Int64;

        DELETE FROM users 
        WHERE telegram_id = $telegram_id;
        """,
        {
            "$telegram_id": (telegram_id, ydb.PrimitiveType.Int64),
        }
    )
    print("User deleted successfully!")


async def get_all_users(pool: ydb.aio.QuerySessionPool):
    """
    Получение всех пользователей (для больших объемов данных использовать с осторожностью)
    """
    print("\nGetting all users...")
    
    async def callee(session: ydb.aio.QuerySession):
        query = """SELECT * FROM users ORDER BY telegram_id;"""
        
        async with await session.transaction(ydb.QuerySnapshotReadOnly()).execute(
            query,
            commit_tx=True,
        ) as result_sets:
            users = []
            async for result_set in result_sets:
                for row in result_set.rows:
                    users.append({
                        'telegram_id': row.telegram_id,
                        'first_name': row.first_name,
                        'username': row.username,
                        'gender': row.gender,
                        'gender_search': row.gender_search,
                        'country': row.country,
                        'country_local': row.country_local,
                        'city': row.city,
                        'city_local': row.city_local,
                        'photo_id': row.photo_id,
                        'about_me': row.about_me,
                        'eighteen_years_and_approval': row.eighteen_years_and_approval,
                        'incognito_pay': row.incognito_pay,
                        'incognito_switch': row.incognito_switch,
                        'banned': row.banned
                    })
            return users
    
    return await pool.retry_operation_async(callee)


async def ban_user(pool: ydb.aio.QuerySessionPool, telegram_id: int):
    """
    Заблокировать пользователя
    """
    await update_user(pool, telegram_id, banned=True)
    print(f"User {telegram_id} has been banned")


async def unban_user(pool: ydb.aio.QuerySessionPool, telegram_id: int):
    """
    Разблокировать пользователя
    """
    await update_user(pool, telegram_id, banned=False)
    print(f"User {telegram_id} has been unbanned")


async def main():
    """
    Пример использования функций
    """
    # Настройки подключения из конфига
    endpoint = YDB_ENDPOINT
    database = YDB_PATH
    token = YDB_TOKEN
    
    # Создание соединения
    driver = await create_connection(endpoint, database, token)
    
    try:
        async with ydb.aio.QuerySessionPool(driver) as pool:
            # Создание таблицы
            await create_users_table(pool)
            
            # Добавление пользователя
            await insert_user(
                pool,
                telegram_id=123456789,
                first_name="John",
                username="john_doe",
                gender="male",
                gender_search="female",
                country="USA",
                country_local="США",
                city="New York",
                city_local="Нью-Йорк",
                about_me="Hello, I'm John!",
                eighteen_years_and_approval=True,
                incognito_pay=False,
                incognito_switch=False,
                banned=False
            )
            
            # Получение пользователя
            user = await get_user_by_telegram_id(pool, 123456789)
            
            # Обновление пользователя
            await update_user(
                pool, 
                123456789, 
                about_me="Updated bio",
                city="Los Angeles"
            )
            
            # Блокировка пользователя
            await ban_user(pool, 123456789)
            
            # Разблокировка пользователя
            await unban_user(pool, 123456789)
            
            # Получение всех пользователей
            all_users = await get_all_users(pool)
            print(f"Total users: {len(all_users)}")
            
    finally:
        await driver.stop()


if __name__ == "__main__":
    # Токен теперь берется из config.py
    asyncio.run(main())