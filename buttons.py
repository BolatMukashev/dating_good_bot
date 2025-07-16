from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import random
from models import ReactionType
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from uuid import uuid4


__all__ = ['get_approval_button',
           'get_btn_to_search',
           'get_matches_menu_buttons',
           'get_wants_user',
           'get_matches_user',
           'get_gender_buttons',
           'get_gender_search_buttons',
           'get_profile_edit_buttons',
           'get_retry_registration_button',
           'get_location_button',
           'get_start_button_match_menu',
           'get_start_button_search_menu',
           'payment_keyboard',
           'reload_search']


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
    button0 = InlineKeyboardButton(text=f"💘 Совпадения [{match_count}]", callback_data=f"matches")
    button1 = InlineKeyboardButton(text=f"✨ Коллекция [{collection_count}]", callback_data=f"collection")
    button2 = InlineKeyboardButton(text=f"Свидание [{love_count}]", callback_data=f"who_wants|LOVE")
    button3 = InlineKeyboardButton(text=f"Постель [{sex_count}]", callback_data=f"who_wants|SEX")
    button4 = InlineKeyboardButton(text=f"Общение [{chat_count}]", callback_data=f"who_wants|CHAT")
    button5 = InlineKeyboardButton(text=f"Обновить 🔄", callback_data=f"reload_matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button0], [button1], [button2, button3, button4], [button5]])
    
    return markup


async def get_wants_user(reaction: ReactionType, price: int, priced: bool = False, user_info: dict=None, id_in_cache: int=0):
    if reaction == "LOVE":
        pass
    elif reaction == "SEX":
        pass
    elif reaction == "CHAT":
        pass
    if user_info == None:
        random_user = random.choice(test_db)
        target_tg_id = random_user.get('tg_id', 0)
        target_name = random_user.get('name', '')
        target_username = random_user.get('username', '')
        description = random_user.get('description', '')
        photo_id = random_user.get('photo_id', '')
        caption=f"<b>{target_name}</b>\n<i>{description}</i>"
    else:
        target_name = user_info.get('target_name', '')
        caption = user_info.get('caption', '')
        photo_id = user_info.get('photo_id', '')

    if priced:
        button1 = InlineKeyboardButton(text=f"Добавлено в 💘 Совпадения", callback_data=f"pass")
    else:
        button1 = InlineKeyboardButton(text=f"Добавить в Совпадения {price} ⭐️", callback_data=f"wants_pay|{target_tg_id}|{price}|{reaction}", pay=True)
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"wants_slider|BACK|{id_in_cache}|{reaction}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"wants_slider|NEXT|{id_in_cache}||{reaction}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])

    return photo_id, caption, markup


async def get_matches_user():
    random_user = None
    target_tg_id = random_user.get('tg_id', 0)
    target_name = random_user.get('name', '')
    target_username = random_user.get('username', '')
    description = random_user.get('description', '')
    photo_id = random_user.get('photo_id', '')
    caption=f"<b>{target_name}</b>\n<i>{description}</i>"

    button1 = InlineKeyboardButton(text="✉️ Начать знакомство", callback_data=f"matches_chat|{target_name}|{target_tg_id}", url=f"https://t.me/{target_username}")
    button2 = InlineKeyboardButton(text=" ⬅️ Назад", callback_data=f"matches_back|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="Вперед ➡️", callback_data=f"matches_next|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="⏮️ Вернуться в меню", callback_data=f"matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2, button3], [button4]])
    
    return photo_id, caption, markup


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
    button = InlineKeyboardButton(text="Посмотреть Совпадения", callback_data="start_btn_match_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


async def get_start_button_search_menu():
    # Кнопка Старт Поиска
    button = InlineKeyboardButton(text="Начать поиск", callback_data="start_btn_search_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    return markup


def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить через Telegram Stars ⭐️", pay=True)
    
    return builder.as_markup()