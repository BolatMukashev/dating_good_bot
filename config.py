from dotenv import dotenv_values
from urllib.parse import quote_plus
from enum import Enum
import os


__all__ = ['BOT_API_KEY',
           'WEBHOOK_URL',
           'WEBHOOK_PATH',
           'mode',
           'LOCAL_WEBHOOK',
           'ADMINS',
           'ADMIN_ID',
           'ASTANA_ID',
           'MIN_COUNT_SYMBOLS',
           'MAX_COUNT_SYMBOLS',
           'NOTION_SITE',
           'opencagedata_API_KEY',
           'PRICES',
           'Pictures'
           ]

config = dotenv_values(".env")

 # вернет false если Yandex и true если PC
LOCAL_WEBHOOK = os.environ.get("LOCAL_WEBHOOK") or config.get('LOCAL_WEBHOOK', 'false').lower()

if LOCAL_WEBHOOK == 'true':
    TESTING = True
    mode = config.get('BOT_MODE', 'webhook').lower()
    BOT_API_KEY = config.get("FIBLY_DATING_BOT") if not TESTING else config.get("DATING_GOOD_BOT")
    WEBHOOK_NGROK_URL = config.get('WEBHOOK_NGROK_URL')
    W_URL = WEBHOOK_NGROK_URL
    ADMIN_ID = int(config.get("ADMIN_ID"))
    ASTANA_ID = int(config.get("ASTANA_ID"))
    SUPABASE_PASSWORD = config.get("SUPABASE_PASSWORD")
    opencagedata_API_KEY = config.get("opencagedata_API_KEY")
else:
    TESTING = False
    mode = 'webhook'
    BOT_API_KEY = os.environ.get("BOT_API_KEY")
    WEBHOOK_YANDEX_URL = os.environ.get('WEBHOOK_YANDEX_URL')
    W_URL = WEBHOOK_YANDEX_URL
    ADMIN_ID = int(os.environ.get("ADMIN_ID"))
    ASTANA_ID = int(os.environ.get("ASTANA_ID"))
    SUPABASE_PASSWORD = os.environ.get("SUPABASE_PASSWORD")
    opencagedata_API_KEY = os.environ.get("opencagedata_API_KEY")


WEBHOOK_PATH = f"/bot/{BOT_API_KEY}"
WEBHOOK_URL = f"{W_URL}{WEBHOOK_PATH}"

# ngrok http 127.0.0.1:8080 - поднять webhood локально на 8080 порту

# настройка админки
ADMINS = [ADMIN_ID, ASTANA_ID]

# настройка базы данных
SUPABASE_PASSWORD = quote_plus(SUPABASE_PASSWORD)
DATABASE_URL = f"postgresql+asyncpg://postgres:{SUPABASE_PASSWORD}@db.epqowkqlqrigguetfiww.supabase.co:5432/postgres"

# DATABASE_URL = "sqlite+aiosqlite:///my_database.db"

MIN_COUNT_SYMBOLS = 15
MAX_COUNT_SYMBOLS = 100


NOTION_SITE = "https://www.notion.so/bolat-mukashev/dating_good_bot-22fa2ae3a2a3806c8b5cc903786b7336?source=copy_link"


# региональные цены с разделением на развитых и развивающихся стран
PRICES = {'en': {'name': 'английский', 'incognito': 100, 'add_to_collection': 40},
          'de': {'name': 'немецкий', 'incognito': 100, 'add_to_collection': 40},
          'fr': {'name': 'французский', 'incognito': 100, 'add_to_collection': 40},
          'it': {'name': 'итальянский', 'incognito': 100, 'add_to_collection': 40},
          'es': {'name': 'испанский', 'incognito': 100, 'add_to_collection': 40},
          'nl': {'name': 'нидерландский', 'incognito': 100, 'add_to_collection': 40},
          'sv': {'name': 'шведский', 'incognito': 100, 'add_to_collection': 40},
          'fi': {'name': 'финский', 'incognito': 100, 'add_to_collection': 40},
          'no': {'name': 'норвежский', 'incognito': 100, 'add_to_collection': 40},
          'he': {'name': 'иврит', 'incognito': 100, 'add_to_collection': 40},
          'ko': {'name': 'корейский', 'incognito': 100, 'add_to_collection': 40},
          'ja': {'name': 'японский', 'incognito': 100, 'add_to_collection': 40},
          'cs': {'name': 'чешский', 'incognito': 100, 'add_to_collection': 40},
          'sk': {'name': 'словацкий', 'incognito': 100, 'add_to_collection': 40},
          'sl': {'name': 'словенский', 'incognito': 100, 'add_to_collection': 40},
          'pl': {'name': 'польский', 'incognito': 100, 'add_to_collection': 40},
          'pt': {'name': 'португальский', 'incognito': 100, 'add_to_collection': 40},
          'pt-br': {'name': 'португальский (бразильский)', 'incognito': 100, 'add_to_collection': 40},
          'hr': {'name': 'хорватский', 'incognito': 100, 'add_to_collection': 40},

          'ru': {'name': 'русский', 'incognito': 50, 'add_to_collection': 20},
          'ar': {'name': 'арабский', 'incognito': 50, 'add_to_collection': 20},
          'be': {'name': 'белорусский', 'incognito': 50, 'add_to_collection': 20},
          'ca': {'name': 'каталанский', 'incognito': 50, 'add_to_collection': 20},
          'hu': {'name': 'венгерский', 'incognito': 50, 'add_to_collection': 20},
          'id': {'name': 'индонезийский', 'incognito': 50, 'add_to_collection': 20},
          'kk': {'name': 'казахский', 'incognito': 50, 'add_to_collection': 20},
          'ms': {'name': 'малайский', 'incognito': 50, 'add_to_collection': 20},
          'fa': {'name': 'персидский', 'incognito': 50, 'add_to_collection': 20},
          'ro': {'name': 'румынский', 'incognito': 50, 'add_to_collection': 20},
          'sr': {'name': 'сербский', 'incognito': 50, 'add_to_collection': 20},
          'tr': {'name': 'турецкий', 'incognito': 50, 'add_to_collection': 20},
          'uk': {'name': 'украинский', 'incognito': 50, 'add_to_collection': 20},
          'uz': {'name': 'узбекский', 'incognito': 50, 'add_to_collection': 20},
          'hi': {'name': 'хинди', 'incognito': 50, 'add_to_collection': 20},
          'vi': {'name': 'вьетнамский', 'incognito': 50, 'add_to_collection': 20},
          'th': {'name': 'тайский', 'incognito': 50, 'add_to_collection': 20},
          'zh': {'name': 'китайский', 'incognito': 50, 'add_to_collection': 20},
          'zh-hans': {'name': 'китайский (упрощенный)', 'incognito': 50, 'add_to_collection': 20},
          'zh-hant': {'name': 'китайский (традиционный)', 'incognito': 50, 'add_to_collection': 20},
          'el': {'name': 'греческий', 'incognito': 50, 'add_to_collection': 20},
          }

# хранилища file_id для продакшена
class Pictures_Prod(str, Enum):
    USER_PROFILE_PICTURE = "AgACAgIAAxkBAAMVaKGT-YS_kjeJWJ2YUcvCSzQPLM4AAk35MRusuAhJ7JHdGZsONPMBAAMCAAN5AAM2BA"
    NO_USERNAME_PICTURE = "AgACAgIAAxkBAAMDaKGSr94mo2yi-MwUTnOrOK4PQU4AAj35MRusuAhJvHFoJ7qnFjwBAAMCAAN5AAM2BA"
    MATCH_MENU_PICTURE = "AgACAgIAAxkBAAMFaKGSv3AMFu9KcaDXw4FaDCQznH4AAj75MRusuAhJb0kk6bVxL8EBAAMCAAN5AAM2BA"
    MATCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMHaKGSxUqGbLwJW1opSara-SU7Yh4AAj_5MRusuAhJDCDp2wRkoBYBAAMCAAN5AAM2BA"
    COLLECTION_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMRaKGT8B_NUtLka7njDxriXYg9MXIAAkv5MRusuAhJ2gz72dihw5IBAAMCAAN5AAM2BA"
    SEX_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMNaKGT5tDESiVB9_45PKER_yHV14YAAkn5MRusuAhJ2kZUaA0usYQBAAMCAAN5AAM2BA"
    LOVE_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMPaKGT7FOQvMVRQmkG_IXzhRmKxukAAkr5MRusuAhJAid4qvonsmABAAMCAAN5AAM2BA"
    CHAT_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMLaKGT4ir--a3uF18V1_HQjmov_MYAAkj5MRusuAhJLG80UoKrN34BAAMCAAN5AAM2BA"
    SEARCH_MENU_PICTURE = "AgACAgIAAxkBAAMJaKGT3ZgihB9C0AtFKMuOt-G6_mEAAkf5MRusuAhJ8NQO33rZ1NUBAAMCAAN5AAM2BA"
    SEARCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMbaKGUEsQeOhHoz79XJsRjqcp8QoYAAlH5MRusuAhJcRwlfZJgKQ0BAAMCAAN5AAM2BA"
    TECHNICAL_WORK = "AgACAgIAAxkBAAMXaKGT_hj7GqZJD6nWmSytTKLccb4AAk75MRusuAhJYdQvHsYYQboBAAMCAAN5AAM2BA"
    CLEANING = "AgACAgIAAxkBAAMTaKGT9IdOHAPuaiiJushDOyBAGksAAkz5MRusuAhJlo_8NWfcVMgBAAMCAAN5AAM2BA"
    TEST_WOMAN_PHOTO = 'AgACAgIAAxkBAAOCaKmlRELVQSWTwe8fYiAOG0ATb48AAvv6MRtWY0hJaF7Nb2KgvR4BAAMCAAN5AAM2BA'
    TEST_MAN_PHOTO = 'AgACAgIAAxkBAAOEaKmlTfk_zoowi3nvLn0H6nBjA0wAAvz6MRtWY0hJCGHdJY2l2KMBAAMCAAN5AAM2BA'

    @classmethod
    def get_not_found_picture(cls, keyword: str):
        key = f"{keyword.upper()}_NOT_FOUND_PICTURE"
        try:
            return cls[key]
        except KeyError:
            raise ValueError(f"No picture found for keyword: {keyword}")


# хранилища file_id для тест бота
class Pictures_Test(str, Enum):
    USER_PROFILE_PICTURE = "AgACAgIAAxkBAAIHUmihnp07R9qzJmSZDQiKfspQMiS7AAJN-TEbrLgISa2RL3L-kX4CAQADAgADeQADNgQ"
    NO_USERNAME_PICTURE = "AgACAgIAAxkBAAIHQGihnmSZtz4ceRZ5dWvcwR9FOxnxAAI9-TEbrLgISUN4AWiAd8FKAQADAgADeQADNgQ"
    MATCH_MENU_PICTURE = "AgACAgIAAxkBAAIHQmihnmlZHDwPoZn2w3EpKAqUlRJwAAI--TEbrLgISV8Cv1wtZJjWAQADAgADeQADNgQ"
    MATCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIHRGihnm1Nq0CrlWkd8Sf7W3WpMNgLAAI_-TEbrLgISaE_Bxgk7I5WAQADAgADeQADNgQ"
    COLLECTION_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIHTmihnpMMit3k05vXMyJrc_-LSdrnAAJL-TEbrLgISXfHufnYPf-fAQADAgADeQADNgQ"
    SEX_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIHSmihnnvGMCgwY3C7oj85ORqBswxFAAJJ-TEbrLgISQVGkZUDFrrrAQADAgADeQADNgQ"
    LOVE_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIHTGihno4AAVeL0K4waDaFalG7c3p8zAACSvkxG6y4CElfqy7UbLRX1AEAAwIAA3kAAzYE"
    CHAT_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIHSGihnne5JYTG5uRe6EC5W2gkFc4AA0j5MRusuAhJrsFAqRZLm9cBAAMCAAN5AAM2BA"
    SEARCH_MENU_PICTURE = "AgACAgIAAxkBAAIHRmihnnIllJMVDgSicW6m4-ZfzMcJAAJH-TEbrLgIScllbfZFk7rwAQADAgADeQADNgQ"
    SEARCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIHVmihnq1CVVuIrAoYRToT1obAHhPBAAJR-TEbrLgISSseECDUyKDcAQADAgADeQADNgQ"
    TECHNICAL_WORK = "AgACAgIAAxkBAAIHVGihnqm5KJQ7Ca7ExH653K2I-PkHAAJO-TEbrLgIST0X30t2oBWvAQADAgADeQADNgQ"
    CLEANING = "AgACAgIAAxkBAAIHUGihnpdOoJjL_rerlt9wfUqAFPLVAAJM-TEbrLgISXHM9RXBqrniAQADAgADeQADNgQ"
    TEST_WOMAN_PHOTO = 'AgACAgIAAxkBAAIHamippc9sfn7tJyE5T1ObMBA48vWLAAL7-jEbVmNISUraejU8gaXpAQADAgADeQADNgQ'
    TEST_MAN_PHOTO = 'AgACAgIAAxkBAAIHbGippdbmtdhVtvS2JWncbLGC3uD1AAL8-jEbVmNISeKz3YI3q8qXAQADAgADeQADNgQ'

    @classmethod
    def get_not_found_picture(cls, keyword: str):
        key = f"{keyword.upper()}_NOT_FOUND_PICTURE"
        try:
            return cls[key]
        except KeyError:
            raise ValueError(f"No picture found for keyword: {keyword}")


# выбор источника
Pictures = Pictures_Test if TESTING else Pictures_Prod

