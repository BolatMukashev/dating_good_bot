from dotenv import dotenv_values
from urllib.parse import quote_plus
from enum import Enum


__all__ = ['BOT_API_KEY',
           'ADMIN_ID',
           'MIN_COUNT_SYMBOLS',
           'MAX_COUNT_SYMBOLS',
           'PRICES',
           'NOTION_SITE',
           'opencagedata_API_KEY',
           'Pictures'
           ]


NOTION_SITE = "https://www.notion.so/bolat-mukashev/dating_good_bot-22fa2ae3a2a3806c8b5cc903786b7336?source=copy_link"

config = dotenv_values(".env")

BOT_API_KEY = config.get("BOT_API_KEY")
ADMIN_ID = int(config.get("ADMIN_ID"))

SUPABASE_PASSWORD = config.get("SUPABASE_PASSWORD")
SUPABASE_PASSWORD = quote_plus(SUPABASE_PASSWORD)
DATABASE_URL = f"postgresql+asyncpg://postgres:{SUPABASE_PASSWORD}@db.epqowkqlqrigguetfiww.supabase.co:5432/postgres"

# DATABASE_URL = "sqlite+aiosqlite:///my_database.db"

opencagedata_API_KEY = config.get("opencagedata_API_KEY")

MIN_COUNT_SYMBOLS = 15
MAX_COUNT_SYMBOLS = 100


# региональные цены с разделением на развитых и развивающихся стран
PRICES = {'en': {'name': 'английский', 'incognito': 2, 'add_to_collection': 2},
          'de': {'name': 'немецкий', 'incognito': 2, 'add_to_collection': 2},
          'fr': {'name': 'французский', 'incognito': 2, 'add_to_collection': 2},
          'it': {'name': 'итальянский', 'incognito': 2, 'add_to_collection': 2},
          'es': {'name': 'испанский', 'incognito': 2, 'add_to_collection': 2},
          'nl': {'name': 'нидерландский', 'incognito': 2, 'add_to_collection': 2},
          'sv': {'name': 'шведский', 'incognito': 2, 'add_to_collection': 2},
          'fi': {'name': 'финский', 'incognito': 2, 'add_to_collection': 2},
          'no': {'name': 'норвежский', 'incognito': 2, 'add_to_collection': 2},
          'he': {'name': 'иврит', 'incognito': 2, 'add_to_collection': 2},
          'ko': {'name': 'корейский', 'incognito': 2, 'add_to_collection': 2},
          'ja': {'name': 'японский', 'incognito': 2, 'add_to_collection': 2},
          'cs': {'name': 'чешский', 'incognito': 2, 'add_to_collection': 2},
          'sk': {'name': 'словацкий', 'incognito': 2, 'add_to_collection': 2},
          'sl': {'name': 'словенский', 'incognito': 2, 'add_to_collection': 2},
          'pl': {'name': 'польский', 'incognito': 2, 'add_to_collection': 2},
          'pt': {'name': 'португальский', 'incognito': 2, 'add_to_collection': 2},
          'pt-br': {'name': 'португальский (бразильский)', 'incognito': 2, 'add_to_collection': 2},
          'hr': {'name': 'хорватский', 'incognito': 2, 'add_to_collection': 2},

          'ru': {'name': 'русский', 'incognito': 1, 'add_to_collection': 1},
          'ar': {'name': 'арабский', 'incognito': 1, 'add_to_collection': 1},
          'be': {'name': 'белорусский', 'incognito': 1, 'add_to_collection': 1},
          'ca': {'name': 'каталанский', 'incognito': 1, 'add_to_collection': 1},
          'hu': {'name': 'венгерский', 'incognito': 1, 'add_to_collection': 1},
          'id': {'name': 'индонезийский', 'incognito': 1, 'add_to_collection': 1},
          'kk': {'name': 'казахский', 'incognito': 1, 'add_to_collection': 1},
          'ms': {'name': 'малайский', 'incognito': 1, 'add_to_collection': 1},
          'fa': {'name': 'персидский', 'incognito': 1, 'add_to_collection': 1},
          'ro': {'name': 'румынский', 'incognito': 1, 'add_to_collection': 1},
          'sr': {'name': 'сербский', 'incognito': 1, 'add_to_collection': 1},
          'tr': {'name': 'турецкий', 'incognito': 1, 'add_to_collection': 1},
          'uk': {'name': 'украинский', 'incognito': 1, 'add_to_collection': 1},
          'uz': {'name': 'узбекский', 'incognito': 1, 'add_to_collection': 1},
          'hi': {'name': 'хинди', 'incognito': 1, 'add_to_collection': 1},
          'vi': {'name': 'вьетнамский', 'incognito': 1, 'add_to_collection': 1},
          'th': {'name': 'тайский', 'incognito': 1, 'add_to_collection': 1},
          'zh': {'name': 'китайский', 'incognito': 1, 'add_to_collection': 1},
          'zh-hans': {'name': 'китайский (упрощенный)', 'incognito': 1, 'add_to_collection': 1},
          'zh-hant': {'name': 'китайский (традиционный)', 'incognito': 1, 'add_to_collection': 1},
          'el': {'name': 'греческий', 'incognito': 1, 'add_to_collection': 1},
          }


# TODO переписать значения при переходе на другого бота
class Pictures(str, Enum):
    USER_PROFILE_PICTURE = "AgACAgIAAxkBAAIF4WiEekZkLaEqAh92-gNw7-Y7qZ-dAALG8TEbvvspSJ0w-8wQRPEDAQADAgADeQADNgQ"
    NO_USERNAME_PICTURE = "AgACAgIAAxkBAAIF5WiEfK_iCKEJ8QFZG6dMrTCPBTEHAALO8TEbvvspSBNkpiJH3ysJAQADAgADeQADNgQ"

    MATCH_MENU_PICTURE = "AgACAgIAAxkBAAIF42iEeoyVyX4q0_7qP8_7-jdDLu9CAALH8TEbvvspSIreTVxnwpvVAQADAgADeQADNgQ"
    MATCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIGEWiFwE1GY12FbRXHVQaBD48Lp7dfAALX9TEbGZ8wSBpGooCFxBlsAQADAgADeQADNgQ"
    COLLECTION_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF62iEipVc6wSozoF5jDz4veHp0I4XAAIs-TEbSuspSH54cCZ4Juw1AQADAgADeQADNgQ"
    SEX_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF6WiEguEcvxB1YoaFMXDGA-fa4KufAAL08TEbvvspSPevawABfmyhnAEAAwIAA3kAAzYE"
    LOVE_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF6GiEgsxqhfqZ-cKM10qWMGTusmwoAAI89jEbhbIhSKDJIrMj60CUAQADAgADeQADNgQ"
    CHAT_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF6miEgvm-FhW9-GUht4xepkL1wT2UAAL18TEbvvspSFRe9R-iLDWnAQADAgADeQADNgQ"

    SEARCH_MENU_PICTURE = "AgACAgIAAxkBAAIF52iEgJy1mLk8fDvsB2uA2-slCXkMAALg8TEbvvspSCFw2YgopGH3AQADAgADeQADNgQ"
    SEARCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF9miEnSrHkCidRcpTxPqKNztY0py0AALf8jEbvvspSFIhwRpoR7CNAQADAgADeQADNgQ"

    @classmethod
    def get_not_found_picture(cls, keyword: str):
        key = f"{keyword.upper()}_NOT_FOUND_PICTURE"
        try:
            return cls[key]
        except KeyError:
            raise ValueError(f"No picture found for keyword: {keyword}")

