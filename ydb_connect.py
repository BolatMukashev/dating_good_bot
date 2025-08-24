import ydb
from config import YDB_ENDPOINT, YDB_PATH, YDB_TOKEN

# Указываем endpoint и путь к базе

# Драйвер
driver = ydb.Driver(
    endpoint=YDB_ENDPOINT,
    database=YDB_PATH,
    credentials=ydb.AccessTokenCredentials(YDB_TOKEN) # ✅ будет брать из переменных окружения
    # credentials=ydb.iam.MetadataUrlCredentials()  # автоматом берёт из метаданных VM/Cloud Function
)


# Запускаем драйвер
driver.wait(fail_fast=True, timeout=30)
session = driver.table_client.session().create()


# --- Создание таблицы ---
def create_table():
    session.create_table(
        f"{YDB_PATH}/users",   # ✅ полный путь
        ydb.TableDescription()
        .with_primary_keys("id")
        .with_columns(
            ydb.Column("id", ydb.PrimitiveType.Int64),
            ydb.Column("name", ydb.PrimitiveType.Utf8),
        )
    )
    print("Таблица 'users' создана")

# --- Вставка данных ---
def insert_row():
    query = f"""
    UPSERT INTO `{YDB_PATH}/users` (id, name)
    VALUES (2, "Bolat");
    """
    session.transaction().execute(query, commit_tx=True)
    print("Данные вставлены")

# --- Чтение данных ---
def select_rows():
    query = f"SELECT id, name FROM `{YDB_PATH}/users`;"
    result = session.transaction().execute(query, commit_tx=True)
    for row in result[0].rows:
        print(row)

# --- Запуск ---
create_table()
insert_row()
select_rows()
driver.stop()
