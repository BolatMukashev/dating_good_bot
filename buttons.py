from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import random
from test_db import test_db
from models import ReactionType
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


__all__ = ['get_18yes_buttons',
           'get_random_user',
           'get_matches_menu_buttons',
           'get_wants_user',
           'get_matches_user',
           'get_gender_buttons',
           'get_gender_search_buttons',
           'get_profile_edit_buttons',
           'get_retry_registration_button',
           'get_location_button',
           'get_start_match_menu_button',
           'get_start_search_menu_button']


async def get_18yes_buttons():
    # Кнопка 18+
    button = InlineKeyboardButton(text="Мне больше 18 лет", callback_data="18yes")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return markup


async def get_random_user():
    # получить случайного тест пользователя
    random_user = random.choice(test_db)
    target_tg_id = random_user.get('tg_id', 0)
    target_name = random_user.get('name', '')
    description = random_user.get('description', '')
    photo_id = random_user.get('photo_id', '')
    caption=f"<b>{target_name}</b>\n<i>{description}</i>"

    button1 = InlineKeyboardButton(text="☕ Свидание", callback_data=f"reaction|LOVE|{target_name}|{target_tg_id}")
    button2 = InlineKeyboardButton(text="👩‍❤️‍💋‍👨 Постель", callback_data=f"reaction|SEX|{target_name}|{target_tg_id}")
    button3 = InlineKeyboardButton(text="💬 Общение", callback_data=f"reaction|CHAT|{target_name}|{target_tg_id}")
    button4 = InlineKeyboardButton(text="Пропустить ⏩", callback_data=f"reaction|SKIP|{target_name}|{target_tg_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1, button2, button3], [button4]])
    
    return photo_id, caption, markup


async def get_matches_menu_buttons():
    # Кнопки match меню
    menu_picture = "AgACAgIAAxkBAAICVmhbrdh8xXXGx6Xy1tr0ouQN0sjFAAIZ8DEbBk3hSoeHxcGbNuBQAQADAgADeQADNgQ"

    button0 = InlineKeyboardButton(text=f"💘 Совпадения [{random.randint(0, 1000)}]", callback_data=f"matches")
    button1 = InlineKeyboardButton(text=f"Свидание [{random.randint(0, 1000)}]", callback_data=f"who_wants|LOVE")
    button2 = InlineKeyboardButton(text=f"Постель [{random.randint(0, 1000)}]", callback_data=f"who_wants|SEX")
    button3 = InlineKeyboardButton(text=f"Общение [{random.randint(0, 1000)}]", callback_data=f"who_wants|CHAT")
    button4 = InlineKeyboardButton(text=f"Обновить 🔄", callback_data=f"reload_matches_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button0], [button1, button2, button3], [button4],])
    
    return menu_picture, markup


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
    random_user = random.choice(test_db)
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
    # Кнопки выбора пола
    button1 = InlineKeyboardButton(text="Мужчина", callback_data="MAN")
    button2 = InlineKeyboardButton(text="Женщина", callback_data="WOMAN")
    button3 = InlineKeyboardButton(text="Другое", callback_data="ANY")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    return markup


async def get_gender_search_buttons():
    # Кнопки выбора поиска пола
    button1 = InlineKeyboardButton(text="Ищу Мужчину", callback_data="search_man")
    button2 = InlineKeyboardButton(text="Ищу Женщину", callback_data="search_woman")
    button3 = InlineKeyboardButton(text="Пол не имеет значения", callback_data="search_any")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]])
    return markup


async def get_profile_edit_buttons():
    # Кнопки выбора поиска пола
    button1 = InlineKeyboardButton(text="Изменить анкету ✏", callback_data="profile_edit")
    button2 = InlineKeyboardButton(text="Стать Инкогнито 🫥", callback_data="incognito_on")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])
    return markup


async def get_retry_registration_button():
    # Кнопки повтора регистрации, если нет username
    button1 = InlineKeyboardButton(text="Повторить регистрацию 🔄", callback_data="retry_registration")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button1]])
    return markup


async def get_location_button():
    # Кнопка отправки геолокации (не инлайн)
    kb = [[KeyboardButton(text="📍 Отправить местоположение", request_location=True)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажми на кнопку"
    )
    return keyboard


async def get_start_match_menu_button():
    # Кнопка старт у меню Совпадений
    button = InlineKeyboardButton(text="Посмотреть Совпадения", callback_data="start_match_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return markup


async def get_start_search_menu_button():
    # Кнопка старт у меню Совпадений
    button = InlineKeyboardButton(text="Начать поиск", callback_data="start_search_menu")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return markup