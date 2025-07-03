from dotenv import dotenv_values

config = dotenv_values(".env")

BOT_API_KEY = config.get("BOT_API_KEY")
ADMIN_ID = config.get("ADMIN_ID")
MONGO_DB_USERNAME = config.get("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = config.get("MONGO_DB_PASSWORD")


MIN_COUNT_SYMBOLS = 15
MAX_COUNT_SYMBOLS = 100