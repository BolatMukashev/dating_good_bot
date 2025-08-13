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
           'Pictures',
           ]


NOTION_SITE = "https://www.notion.so/bolat-mukashev/dating_good_bot-22fa2ae3a2a3806c8b5cc903786b7336?source=copy_link"

config = dotenv_values(".env")

BOT_API_KEY = config.get("BOT_API_KEY")

ADMIN_ID = int(config.get("ADMIN_ID"))
ASTANA_ID = int(config.get("ASTANA_ID"))

SUPABASE_PASSWORD = config.get("SUPABASE_PASSWORD")
SUPABASE_PASSWORD = quote_plus(SUPABASE_PASSWORD)
DATABASE_URL = f"postgresql+asyncpg://postgres:{SUPABASE_PASSWORD}@db.epqowkqlqrigguetfiww.supabase.co:5432/postgres"

# DATABASE_URL = "sqlite+aiosqlite:///my_database.db"

opencagedata_API_KEY = config.get("opencagedata_API_KEY")

MIN_COUNT_SYMBOLS = 15
MAX_COUNT_SYMBOLS = 100


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

          'ru': {'name': 'русский', 'incognito': 1, 'add_to_collection': 1},
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


class Pictures(str, Enum):
    USER_PROFILE_PICTURE = "AgACAgIAAxkBAAMiaJxa0dQVZthIi_kbJaXuqej4GssAAiH0MRuvyuFIBIO4V3QCS3YBAAMCAAN5AAM2BA"
    NO_USERNAME_PICTURE = "AgACAgIAAxkBAAMIaJxAHuWUqFut_wOnjyTKNxc_eDMAAojzMRuvyuFI5Qgnhxtse1EBAAMCAAN5AAM2BA"

    MATCH_MENU_PICTURE = "AgACAgIAAxkBAAMKaJxApj48PAjaqcBVWCqQip4DxrgAApDzMRuvyuFI0N92yY6UvTIBAAMCAAN5AAM2BA"
    MATCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMMaJxAsFW1DLyOWOL4qKt49qkas9IAApHzMRuvyuFIAAFt0AnDkB-yAQADAgADeQADNgQ"
    COLLECTION_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMeaJxGVn9CXUbAX0XIbxOb8cYs2PEAArnzMRuvyuFIVt5QFJ2Z6wcBAAMCAAN5AAM2BA"
    SEX_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMSaJxEUqb56MXhUkx8nYzwrTqvvPMAAqfzMRuvyuFImjoMmXrqjZ4BAAMCAAN5AAM2BA"
    LOVE_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMUaJxEVlZvRfFD5wXfHzDxhJwDj8QAAqjzMRuvyuFIcuinXW0gIwQBAAMCAAN5AAM2BA"
    CHAT_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMQaJxETV0sR8T-8zBNB-g9N-VHWVQAAqbzMRuvyuFIx-ayp4M6MIsBAAMCAAN5AAM2BA"

    SEARCH_MENU_PICTURE = "AgACAgIAAxkBAAMOaJxAuBMKJ5AXa0iw-vWpM-H7VAkAApLzMRuvyuFIjn8R8OK9HxwBAAMCAAN5AAM2BA"
    SEARCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAMcaJxEaLOjs8pjY_eTF14zKiH2TXIAAqzzMRuvyuFIN7kctorOcFMBAAMCAAN5AAM2BA"

    TECHNICAL_WORK = "AgACAgIAAxkBAAMYaJxEX6Yd4h9z9BK7PhE6vo5fYy4AAqrzMRuvyuFIteQ2xTmUjNABAAMCAAN5AAM2BA"
    CLEANING = "AgACAgIAAxkBAAMWaJxEWrJrqP_CiBhd33AxpGgcHM8AAqnzMRuvyuFIGVdDbGybAj0BAAMCAAN5AAM2BA"

    @classmethod
    def get_not_found_picture(cls, keyword: str):
        key = f"{keyword.upper()}_NOT_FOUND_PICTURE"
        try:
            return cls[key]
        except KeyError:
            raise ValueError(f"No picture found for keyword: {keyword}")


# class PicturesTEST(str, Enum):
#     USER_PROFILE_PICTURE = "AgACAgIAAxkBAAIF4WiEekZkLaEqAh92-gNw7-Y7qZ-dAALG8TEbvvspSJ0w-8wQRPEDAQADAgADeQADNgQ"
#     NO_USERNAME_PICTURE = "AgACAgIAAxkBAAIF5WiEfK_iCKEJ8QFZG6dMrTCPBTEHAALO8TEbvvspSBNkpiJH3ysJAQADAgADeQADNgQ"

#     MATCH_MENU_PICTURE = "AgACAgIAAxkBAAIF42iEeoyVyX4q0_7qP8_7-jdDLu9CAALH8TEbvvspSIreTVxnwpvVAQADAgADeQADNgQ"
#     MATCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIGEWiFwE1GY12FbRXHVQaBD48Lp7dfAALX9TEbGZ8wSBpGooCFxBlsAQADAgADeQADNgQ"
#     COLLECTION_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF62iEipVc6wSozoF5jDz4veHp0I4XAAIs-TEbSuspSH54cCZ4Juw1AQADAgADeQADNgQ"
#     SEX_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF6WiEguEcvxB1YoaFMXDGA-fa4KufAAL08TEbvvspSPevawABfmyhnAEAAwIAA3kAAzYE"
#     LOVE_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF6GiEgsxqhfqZ-cKM10qWMGTusmwoAAI89jEbhbIhSKDJIrMj60CUAQADAgADeQADNgQ"
#     CHAT_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF6miEgvm-FhW9-GUht4xepkL1wT2UAAL18TEbvvspSFRe9R-iLDWnAQADAgADeQADNgQ"

#     SEARCH_MENU_PICTURE = "AgACAgIAAxkBAAIF52iEgJy1mLk8fDvsB2uA2-slCXkMAALg8TEbvvspSCFw2YgopGH3AQADAgADeQADNgQ"
#     SEARCH_NOT_FOUND_PICTURE = "AgACAgIAAxkBAAIF9miEnSrHkCidRcpTxPqKNztY0py0AALf8jEbvvspSFIhwRpoR7CNAQADAgADeQADNgQ"

#     TECHNICAL_WORK = "AgACAgIAAxkBAAIG3miTKK35xSZwhBHvSvin06vNH7rYAAJm8DEbH5uYSJqRLKwys2yfAQADAgADeQADNgQ"
#     CLEANING = "AgACAgIAAxkBAAIG3WiTKJwDRse3hqjVAivbYj9MXs8RAAJl8DEbH5uYSGVJKvSV2lkTAQADAgADeQADNgQ"

#     @classmethod
#     def get_not_found_picture(cls, keyword: str):
#         key = f"{keyword.upper()}_NOT_FOUND_PICTURE"
#         try:
#             return cls[key]
#         except KeyError:
#             raise ValueError(f"No picture found for keyword: {keyword}")

