from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

async def get_18yes_buttons():
    button = InlineKeyboardButton(text="Мне больше 18 лет", callback_data="18yes")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return markup