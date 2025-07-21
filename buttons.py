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
           'reload_search',
           'empty_category_buttons',
           'get_collection_user']


async def get_approval_button():
    # Кнопка 18+ и согласие с политикой и соглашением
    button = InlineKeyboardButton(text="Начать регистрацию", callback_data="18yes_and_approval")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def reload_search():
    # Кнопка обновить поиск
    button = InlineKeyboardButton(text="Обновить 🔄", callback_data="reload_search")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def get_btn_to_search(target_name, target_tg_id):
    # получить кнопки для поиска
    button1 = InlineKeyboardButton(text="☕ Свидание", callback_data=f"reaction|LOVE|{target_name}|{target_tg_id}")
    button2 = InlineKeyboardButton(text="👩‍❤️‍💋‍👨 Постель", callback_data=f"reaction|SEX|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="💬 Общение", callback_data=f"reaction|CHAT|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="Пропустить ⏩", callback_data=f"reaction|SKIP|{target_name}|{target_tg_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1, button2, button3], [button4]])
    
    return markup


async def get_matches_menu_buttons(match_count: int, collection_count: int, love_count: int, sex_count: int, chat_count: int):
    # Кнопки match меню

    unique_suffix = uuid4().hex[:4]
    button0 = InlineKeyboardButton(text=f"💘 Совпадения [{match_count}]", callback_data=f"matches")
    button1 = InlineKeyboardButton(text=f"✨ Коллекция [{collection_count}]", callback_data=f"collection")
    button2 = InlineKeyboardButton(text=f"Свидание [{love_count}]", callback_data=f"intentions|LOVE")
    button3 = InlineKeyboardButton(text=f"Постель [{sex_count}]", callback_data=f"intentions|SEX")
    button4 = InlineKeyboardButton(text=f"Общение [{chat_count}]", callback_data=f"intentions|CHAT")
    button5 = InlineKeyboardButton(text=f"Обновить 🔄", callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button0], [button1], [button2, button3, button4], [button5]])
    
    return markup


async def empty_category_buttons():
    # Пустая категория, выход в меню Совпадений
    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=f"⏮️ Вернуться в меню", callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    
    return markup


async def get_intention_user(user: User, ids: list, reaction: ReactionType, amount: int):
    # получить кнопки для 
    back_id, next_id = ids
    if ids[0] == None:
        back_id = 'pass'
    if ids[1] == None:
        next_id = 'pass'

    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text=f"Добавить в Коллекцию {amount} ⭐️", callback_data=f"pay_intentions|{user.telegram_id}|{amount}|{reaction}", pay=True)
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"navigation_intentions|{reaction}|{back_id}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"navigation_intentions|{reaction}|{next_id}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return markup


async def get_match_user(user: User, ids: list):
    # получить кнопки для 
    back_id, next_id = ids
    if ids[0] == None:
        back_id = 'pass'
    if ids[1] == None:
        next_id = 'pass'

    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text="✉️ Начать знакомство", callback_data=f"pass", url=f"https://t.me/{user.username}")
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"navigation_matches|{back_id}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"navigation_matches|{next_id}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return markup


async def get_collection_user(user: User, ids: list):
    # получить кнопки для 
    back_id, next_id = ids
    if ids[0] == None:
        back_id = 'pass'
    if ids[1] == None:
        next_id = 'pass'

    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text="✉️ Начать знакомство", callback_data=f"pass", url=f"https://t.me/{user.username}")
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"navigation_collection|{back_id}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"navigation_collection|{next_id}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"match_menu_start_btn|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return markup


async def get_gender_buttons():
    # Выбора пола
    button1 = InlineKeyboardButton(text="Мужчина", callback_data="MAN")
    button2 = InlineKeyboardButton(text="Женщина", callback_data="WOMAN")
    button3 = InlineKeyboardButton(text="Другое", callback_data="ANY")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    
    return markup


async def get_gender_search_buttons():
    # Выбора поиска пола
    button1 = InlineKeyboardButton(text="Ищу Мужчину", callback_data="search_man")
    button2 = InlineKeyboardButton(text="Ищу Женщину", callback_data="search_woman")
    button3 = InlineKeyboardButton(text="Пол не имеет значения", callback_data="search_any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    
    return markup


async def get_profile_edit_buttons(pay_status: bool, incognito_switch: bool):
    # Изменение профиля и статуса инкогнито
    if not pay_status:
        status = 'NOT_PAYED'
        btn_text = "Стать Инкогнито 🫥"
    else:
        if incognito_switch:
            status = 'ON'
            btn_text = "Инкогнито включено ✅"
        else:
            status = 'OFF'
            btn_text = "Инкогнито выключено 🚫"
    
    unique_suffix = uuid4().hex[:4]
    button1 = InlineKeyboardButton(text="Изменить анкету ✏", callback_data="profile_edit")
    button2 = InlineKeyboardButton(text=btn_text, callback_data=f"incognito|{status}|{unique_suffix}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])
    
    return markup


async def get_retry_registration_button():
    # Кнопки повтора регистрации, если нет username
    button1 = InlineKeyboardButton(text="Повторить регистрацию 🔄", callback_data="retry_registration")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    
    return markup


async def get_location_button():
    # Отправка геолокации (не инлайн)
    kb = [[KeyboardButton(text="📍 Отправить местоположение", request_location=True)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажми на кнопку")
    
    return keyboard


async def get_start_button_match_menu():
    # Кнопка Старт Посмотреть Совпадения
    button = InlineKeyboardButton(text="Посмотреть Совпадения", callback_data="match_menu_start_btn")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def get_start_button_search_menu():
    # Кнопка Старт Поиска
    button = InlineKeyboardButton(text="Начать поиск", callback_data="search_menu_start_btn")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить через Telegram Stars ⭐️", pay=True)
    
    return builder.as_markup()