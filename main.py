import logging
from db_connect import async_engine, Base
from aiogram.types import InputMediaPhoto, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_API_KEY, ADMIN_ID, MONGO_DB_PASSWORD, MONGO_DB_USERNAME, MIN_COUNT_SYMBOLS, MAX_COUNT_SYMBOLS, USER_PROFILE_PICTURE, MATCH_MENU_PICTURE, SEARCH_MENU_PICTURE
from sqlalchemy.exc import NoResultFound
from models import ReactionType, gender, gender_search, gender_search_db
from buttons import get_18yes_buttons, get_random_user, get_matches_menu_buttons, get_matches_user, get_wants_user, get_gender_buttons, get_gender_search_buttons, get_location_button
from functions import get_cached_message_id, save_to_cache, create_or_update_user, update_user_fields, add_reaction, add_payment, get_location_info, get_user_language
from messages import text


# ------------------------------------------------------------------- Настройка бота -------------------------------------------------------

# TODO Supabase - SQL bd Postgres


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ------------------------------------------------------------------- Анкета пользователя -------------------------------------------------------


# Команда Старт
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    user_lang = await get_user_language(message)

    if not username:
        await message.answer(text[user_lang]['user_profile']['username_error'])
        return
    
    # запись в базу
    await create_or_update_user(user_id, first_name, username)
    caption=text[user_lang]['user_profile']['step_1'].format(first_name=first_name)
    starting_message = await message.answer_photo(photo=USER_PROFILE_PICTURE, caption=caption, parse_mode="HTML", reply_markup=await get_18yes_buttons())
    
    # запись в базу
    await save_to_cache(user_id, "start_message_id", message_id = starting_message.message_id)


# подтверждение 18 лет
@dp.callback_query(F.data == "18yes")
async def query_18years(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)

    # запись в базу
    await update_user_fields(user_id, eighteen_years_old=True)

    # уведомление сверху
    await callback.answer(text=text[user_lang]['notifications']['18year'])

    # 1. Меняем текст сообщения и убираем inline-кнопки
    await callback.message.edit_caption(caption=text[user_lang]['user_profile']['step_2'], parse_mode="HTML", reply_markup=None)

    # 2. Отдельно отправляем сообщение с обычной клавиатурой для геолокации
    location_message = await callback.message.answer(text[user_lang]['user_profile']['get_location_message'],
                                                     reply_markup= await get_location_button(), parse_mode="HTML")
    
    # запись в базу
    await save_to_cache(user_id, "location_message_id", message_id = location_message.message_id)


# подтверждение локации
@dp.message(F.location)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(message)

    latitude = message.location.latitude
    longitude = message.location.longitude

    # 1. Получаем название на языке пользователя (по языку Telegram)
    user_language_code = message.from_user.language_code or 'ru'
    country_local, city_local = await get_location_info(latitude, longitude, lang=user_language_code)

    # 2. Получаем название на английском для записи в базу
    country_en, city_en = await get_location_info(latitude, longitude, lang='en')

    # запись в базу
    await update_user_fields(user_id, country=country_en, city=city_en)
    
    # запись в базу
    await save_to_cache(user_id, "country_local", data = country_local)
    await save_to_cache(user_id, "city_local", data = city_local)

    await message.delete() #удалить сообщение пользователя с локацией

    # получаем id из Кэш и удаляем сообщение
    location_message_id = await get_cached_message_id(user_id, "location_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=location_message_id)

    # изменяем запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")
    await bot.edit_message_caption(chat_id=message.chat.id,
                                   message_id=int(start_message_id),
                                   caption= text[user_lang]['user_profile']['step_3'],
                                   reply_markup = await get_gender_buttons())


@dp.callback_query(F.data.in_(["MAN", "WOMAN", "ANY"]))
async def query_gender(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)

    # запись в базу
    await update_user_fields(user_id, gender=callback.data)
    
    # уведомление сверху
    await callback.answer(text=text[user_lang]['notifications']['gender'].format(user_gender=gender.get(callback.data)))


    # изменяем запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")
    await bot.edit_message_caption(chat_id=callback.chat.id,
                                   message_id=int(start_message_id),
                                   caption= text[user_lang]['user_profile']['step_3'],
                                   reply_markup = await get_gender_buttons())

    await callback.message.edit_text(text="✅ Шаг 3 выполнен")
    await callback.message.answer(text[user_lang]['user_profile']['step_4'], reply_markup= await get_gender_search_buttons())


@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def query_gender_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)
    
    # запись в базу
    await update_user_fields(user_id, gender_search=gender_search_db.get(callback.data))

    # уведомление сверху
    await callback.answer(text=text[user_lang]['notifications']['gender_search'].format(gender_search=gender_search.get(callback.data)))

    await callback.message.edit_text(text="✅ Шаг 4 выполнен")
    await callback.message.answer(text[user_lang]['user_profile']['step_5'], reply_markup=ReplyKeyboardRemove())


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(message)

    photo = message.photo[-1]
    file_id = photo.file_id
    print(file_id)

    # запись в базу
    await update_user_fields(user_id, photo_id = file_id)

    await message.delete()
    await message.answer("✅ Шаг 5 выполнен")
    await message.answer(text[user_lang]['user_profile']['step_6'], parse_mode="HTML")



# ------------------------------------------------------------------ ПОИСК ----------------------------------------------------------


# Команда поиск
@dp.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    photo_id, caption, markup = await get_random_user()
    await message.answer_photo(photo=photo_id, caption=caption, parse_mode="HTML", reply_markup=markup)


# обработка колбека поиска
@dp.callback_query(lambda c: c.data.startswith("reaction"))
async def handle_reaction(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, reaction_str, target_name, target_tg_id = callback.data.split("|", 3)

    try:
        reaction = ReactionType(reaction_str)
    except ValueError:
        await callback.answer("Неизвестная реакция")
        return

    # запись в базу
    await add_reaction(user_id, target_tg_id, reaction_str)

    # уведомление сверху
    await callback.answer(reaction.message_template.format(name=target_name))

    photo_id, caption, markup = await get_random_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, reply_markup=markup, parse_mode="HTML")


# ------------------------------------------------------------------ СОВПАДЕНИЯ ----------------------------------------------------------


# Команда Совпадения
@dp.message(Command("match"))
async def cmd_match(message: types.Message, state: FSMContext):
    menu_picture, markup = await get_matches_menu_buttons()
    await message.answer_photo(photo=menu_picture, parse_mode="HTML", reply_markup=markup)


@dp.callback_query(F.data == "matches")
async def query_matches(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    photo_id, caption, markup = await get_matches_user()
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, reply_markup=markup, parse_mode="HTML")


@dp.callback_query(F.data == "matches_menu")
async def query_matches_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    menu_picture, markup = await get_matches_menu_buttons()
    await callback.message.edit_media(media=InputMediaPhoto(media=menu_picture))
    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query(F.data == "reload_matches_menu")
async def query_reload_matches_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, markup = await get_matches_menu_buttons()
    await callback.message.edit_reply_markup(reply_markup=markup)


# обработка колбека кому нравишься
@dp.callback_query(lambda c: c.data.startswith("who_wants"))
async def handle_who_wants(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, reaction = callback.data.split("|", 1)
    photo_id, caption, markup = await get_wants_user(reaction, 1)
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, reply_markup=markup, parse_mode="HTML")


# ------------------------------------------------------------------- Оплата -------------------------------------------------------


def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить через Telegram Stars ⭐️", pay=True)
    return builder.as_markup()


# обработка колбека оплаты
@dp.callback_query(lambda c: c.data.startswith("wants_pay"))
async def handle_wants_pay(callback: types.CallbackQuery):
    _, target_tg_id, target_name, caption, photo_id, price_str, reaction = callback.data.split("|")
    price = int(price_str)

    prices = [LabeledPrice(label=f"Добавить {target_name} в Совпадения", amount=price)]

    sent_invoice = await callback.message.answer_invoice(
        title=f"Добавить в Совпадения {target_name}",
        description=f"При добавлении в Совпадения, вы получите доступ к профилю {target_name} и сможете ей/ему написать",
        payload=f"payment_ok|{target_tg_id}|{price}|{callback.message.message_id}|{target_name}|{caption}|{photo_id}|{reaction}",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=payment_keyboard()
    )

    # сохраняем в Кэш
    await save_to_cache(callback.from_user.id, "invoice_message_id", message_id = sent_invoice.message_id)

    await callback.answer()


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(lambda message: message.successful_payment is not None)
async def on_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id

    # Пример обработки payload:
    if payload.startswith("payment_ok"):
        _, target_id, price, message_id, target_name, caption, photo_id, reaction = payload.split("|")
        user_info = {"target_name": target_name, "caption": caption, "photo_id": photo_id}

        # запись в базу
        await add_payment(user_id, target_id, price)
    
    # изменяем запись
    markup = await get_wants_user(reaction, 1, priced=True, user_info=user_info)
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=int(message_id), reply_markup=markup)
    
    # получаем id из Кэш и удаляем сообщение
    invoice_message_id = await get_cached_message_id(user_id, "invoice_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=invoice_message_id)


# ------------------------------------------------------------------- Текст (Последний шаг в Анкете)-------------------------------------------------------


# обработка текста - добавляет или изменяет описание "о себе"
@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(message)

    # удаляем сообщение пользователя
    await message.delete()
    text = message.text
    print(text)
    if len(text) >= MIN_COUNT_SYMBOLS and len(text) <= MAX_COUNT_SYMBOLS:

        # запись в базу
        await update_user_fields(user_id, about_me = text)

        await message.answer("✅ Шаг 6 выполнен")
        await message.answer("🔍 Найти партнера - /search" \
        "\n💘Совпадения (match) - /match")

    elif len(text) < MIN_COUNT_SYMBOLS:
        await message.answer(text[user_lang]['user_profile']['min_count_symbols_error'].format(MIN_COUNT_SYMBOLS=MIN_COUNT_SYMBOLS, text_lenght=len(text)))
    elif len(text) > MAX_COUNT_SYMBOLS:
        await message.answer(text[user_lang]['user_profile']['max_count_symbols_error'].format(MAX_COUNT_SYMBOLS=MAX_COUNT_SYMBOLS, text_lenght=len(text)))


# ------------------------------------------------------------------- Активация бота -------------------------------------------------------


async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())