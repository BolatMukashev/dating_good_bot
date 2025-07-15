from dotenv import dotenv_values


__all__ = ['BOT_API_KEY',
           'ADMIN_ID',
           'MONGO_DB_USERNAME',
           'MONGO_DB_PASSWORD',
           'MIN_COUNT_SYMBOLS',
           'MAX_COUNT_SYMBOLS',
           'USER_PROFILE_PICTURE',
           'MATCH_MENU_PICTURE',
           'SEARCH_MENU_PICTURE',
           'NO_USERNAME_PICTURE',
           'PRICE_INCOGNITO',
           'PRICE_ADD_TO_MATCHES',
           'NOT_FOUND_PICTURE',
           'NOTION_SITE',
           'opencagedata_API_KEY'
           ]


NOTION_SITE = "https://www.notion.so/bolat-mukashev/dating_good_bot-22fa2ae3a2a3806c8b5cc903786b7336?source=copy_link"

config = dotenv_values(".env")

BOT_API_KEY = config.get("BOT_API_KEY")
ADMIN_ID = config.get("ADMIN_ID")

MONGO_DB_USERNAME = config.get("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = config.get("MONGO_DB_PASSWORD")

opencagedata_API_KEY = config.get("opencagedata_API_KEY")

MIN_COUNT_SYMBOLS = 15
MAX_COUNT_SYMBOLS = 100

# pictures:
USER_PROFILE_PICTURE = "AgACAgIAAxkBAAIDFWhniNnlg57V82BizYfHc1nBiz3VAALp8jEbg3VAS98yh2TO5O79AQADAgADeQADNgQ"
MATCH_MENU_PICTURE = "AgACAgIAAxkBAAIDG2hniWKMMZHagFbpGe9_Kn2KxTdNAALq8jEbg3VASzK6PDhuBbsYAQADAgADeQADNgQ"
SEARCH_MENU_PICTURE = "AgACAgIAAxkBAAIDHmhniXNyAc8cH4YWgrLDMjjBc2NSAALr8jEbg3VAS8X0z5G5JvcFAQADAgADeQADNgQ"
NO_USERNAME_PICTURE = "AgACAgIAAxkBAAID-WhrlyLSKE5v9lMr7wVc0oLANb1uAAKy-zEb-6ZgS8e530fQZpqXAQADAgADeQADNgQ"
NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIEvmhza0krNzZpfxACmpK6ldTGMiKdAAKb-zEb-GmZS3mUhF5Kg96SAQADAgADeQADNgQ"

#prices:
PRICE_INCOGNITO = 1
PRICE_ADD_TO_MATCHES = 1