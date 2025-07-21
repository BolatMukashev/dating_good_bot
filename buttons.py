from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models import ReactionType, User
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from uuid import uuid4


__all__ = ['get_approval_button',
           'get_btn_to_search',
           'get_matches_menu_buttons',
           'get_intention_user',
           'get_match_user',
           'get_gender_buttons',
           'get_gender_search_buttons',
           'get_profile_edit_buttons',
           'get_retry_registration_button',
           'get_location_button',
           'get_start_button_match_menu',
           'get_start_button_search_menu',
           'payment_keyboard',
           'reload_search_button',
           'empty_category_buttons',
           'get_collection_user']


async def get_approval_button(texts: dict):
    # Кнопка 18+ и согласие с политикой и соглашением
    button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["begin"], callback_data="18yes_and_approval")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def reload_search_button(texts: dict):
    # Кнопка обновить поиск
    button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["reload"], callback_data="reload_search")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def get_btn_to_search(target_name, target_tg_id, texts: dict):
    # получить кнопки для поиска
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["reaction"]['love'], callback_data=f"reaction|LOVE|{target_name}|{target_tg_id}")
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["reaction"]['sex'], callback_data=f"reaction|SEX|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["reaction"]['chat'], callback_data=f"reaction|CHAT|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["reaction"]['skip'], callback_data=f"reaction|SKIP|{target_name}|{target_tg_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1, button2, button3], [button4]])
    
    return markup


async def get_matches_menu_buttons(match_count: int, collection_count: int, love_count: int, sex_count: int, chat_count: int, texts: dict):
    # Кнопки match меню

    unique_suffix = uuid4().hex[:4]
    button0 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['match'].format(match_count=match_count), callback_data=f"matches")
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['collection'].format(collection_count=collection_count), callback_data=f"collection")
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['love'].format(love_count=love_count), callback_data=f"intentions|LOVE")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['sex'].format(sex_count=sex_count), callback_data=f"intentions|SEX")
    button4 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['chat'].format(chat_count=chat_count), callback_data=f"intentions|CHAT")
    button5 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["reload"], callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button0], [button1], [button2, button3, button4], [button5]])
    
    return markup


async def empty_category_buttons(texts: dict):
    # Пустая категория, выход в меню Совпадений
    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["return"], callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    
    return markup


async def get_intention_user(user: User, ids: list, reaction: ReactionType, amount: int, texts: dict):
    # получить кнопки для 
    back_id, next_id = ids
    if ids[0] == None:
        back_id = 'pass'
    if ids[1] == None:
        next_id = 'pass'

    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['add_to_collection'].format(amount=amount), callback_data=f"pay_intentions|{user.telegram_id}|{amount}|{reaction}", pay=True)
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["back"], callback_data=f"navigation_intentions|{reaction}|{back_id}")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["next"], callback_data=f"navigation_intentions|{reaction}|{next_id}")
    button4 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["return"], callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return markup


async def get_match_user(user: User, ids: list, texts: dict):
    # получить кнопки для 
    back_id, next_id = ids
    if ids[0] == None:
        back_id = 'pass'
    if ids[1] == None:
        next_id = 'pass'

    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['send_message'], callback_data=f"pass", url=f"https://t.me/{user.username}")
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["back"], callback_data=f"navigation_matches|{back_id}")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["next"], callback_data=f"navigation_matches|{next_id}")
    button4 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["return"], callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return markup


async def get_collection_user(user: User, ids: list, texts: dict):
    # получить кнопки для 
    back_id, next_id = ids
    if ids[0] == None:
        back_id = 'pass'
    if ids[1] == None:
        next_id = 'pass'

    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]['send_message'], callback_data=f"pass", url=f"https://t.me/{user.username}")
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["back"], callback_data=f"navigation_collection|{back_id}")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["next"], callback_data=f"navigation_collection|{next_id}")
    button4 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["return"], callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return markup


async def get_gender_buttons(texts: dict):
    # Выбора пола
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["gender"]['man'], callback_data="MAN")
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["gender"]['woman'], callback_data="WOMAN")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["gender"]['any'], callback_data="ANY")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    
    return markup


async def get_gender_search_buttons(texts: dict):
    # Выбора поиска пола
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["gender_search"]['man'], callback_data="search_man")
    button2 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["gender_search"]['woman'], callback_data="search_woman")
    button3 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["gender_search"]['any'], callback_data="search_any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    
    return markup


async def get_profile_edit_buttons(pay_status: bool, incognito_switch: bool, texts: dict):
    # Изменение профиля и статуса инкогнито
    if not pay_status:
        status = 'NOT_PAYED'
        btn_text = texts["BUTTONS_TEXT"]["incognito"]["not_active"]
    else:
        if incognito_switch:
            status = 'ON'
            btn_text = texts["BUTTONS_TEXT"]["incognito"]["on"]
        else:
            status = 'OFF'
            btn_text = texts["BUTTONS_TEXT"]["incognito"]["off"]
    
    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["profile"]["edit"], callback_data="profile_edit")
    button2 = InlineKeyboardButton(text=btn_text, callback_data=f"incognito|{status}|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])
    
    return markup


async def get_retry_registration_button(texts: dict):
    # Кнопки повтора регистрации, если нет username
    button1 = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["profile"]["retry"], callback_data="retry_registration")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    
    return markup


async def get_location_button(texts: dict):
    # Отправка геолокации (не инлайн)
    kb = [[KeyboardButton(text=texts["BUTTONS_TEXT"]["location"]["send"], request_location=True)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=texts["BUTTONS_TEXT"]["location"]["press"])
    
    return keyboard


async def get_start_button_match_menu(texts: dict):
    # Кнопка Старт Посмотреть Совпадения
    button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["match_menu"]["start"], callback_data="match_menu_start_btn")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def get_start_button_search_menu(texts: dict):
    # Кнопка Старт Поиска
    button = InlineKeyboardButton(text=texts["BUTTONS_TEXT"]["search_menu"]["start"], callback_data="search_menu_start_btn")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


def payment_keyboard(texts: dict):
    builder = InlineKeyboardBuilder()
    builder.button(text=texts["BUTTONS_TEXT"]["pay"], pay=True)
    
    return builder.as_markup()