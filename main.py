import logging
from db_connect import async_engine
from aiogram.types import InputMediaPhoto, LabeledPrice
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import *
from models import ReactionType, Gender, Base
from buttons import *
from functions import *
from messages import TEXT, GENDER_LABELS, GENDER_SEARCH_LABELS


# ------------------------------------------------------------------- Настройка бота -------------------------------------------------------


# TODO Supabase - SQL bd Postgres
# TODO Больше инфы в анкете, кнопки под описанием
# TODO 2 сообщения после заполнения анкеты


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

    await message.delete() #удалить сообщение пользователя /start

    if not username:
        starting_message = await message.answer_photo(photo=NO_USERNAME_PICTURE,
                                   caption=TEXT[user_lang]['user_profile']['username_error'],
                                   parse_mode="HTML",
                                   reply_markup=await get_retry_registration_button())
    else:
        # запись в базу
        await create_or_update_user(user_id, first_name, username)

        starting_message = await message.answer_photo(photo=USER_PROFILE_PICTURE,
                                                    caption=TEXT[user_lang]['user_profile']['step_1'].format(first_name=first_name),
                                                    parse_mode="HTML",
                                                    reply_markup=await get_18yes_buttons())
    # запись в базу
    await save_to_cache(user_id, "start_message_id", message_id = starting_message.message_id)


# повторная регистрация, если нет username
@dp.callback_query(F.data == "retry_registration")
async def query_retry_registration(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_lang = await get_user_language(callback)

    if not username:
        return
    
    # запись в базу
    await create_or_update_user(user_id, first_name, username)
    
    # изменяем стартовую запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")

    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=int(start_message_id),
                                 media=InputMediaPhoto(media=USER_PROFILE_PICTURE))

    await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                   message_id=int(start_message_id),
                                   caption=TEXT[user_lang]['user_profile']['step_1'].format(first_name=first_name),
                                   reply_markup = await get_18yes_buttons(),
                                   parse_mode="HTML")


# подтверждение 18 лет
@dp.callback_query(F.data == "18yes")
async def query_18years(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)

    # запись в базу
    await update_user_fields(user_id, eighteen_years_old=True)

    # уведомление сверху
    await callback.answer(text=TEXT[user_lang]['notifications']['18year'])

    # 1. Меняем текст сообщения и убираем inline-кнопки
    await callback.message.edit_caption(caption=TEXT[user_lang]['user_profile']['step_2'], parse_mode="HTML", reply_markup=None)

    # 2. Отдельно отправляем сообщение с обычной клавиатурой для геолокации
    location_message = await callback.message.answer(TEXT[user_lang]['user_profile']['get_location_message'],
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
    await update_user_fields(user_id, country=country_en, city=city_en, country_local=country_local, city_local=city_local)
    
    await message.delete() #удалить сообщение пользователя с локацией

    # получаем id из Кэш и удаляем сообщение
    location_message_id = await get_cached_message_id(user_id, "location_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=location_message_id)

    # изменяем запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")
    await bot.edit_message_caption(chat_id=message.chat.id,
                                   message_id=int(start_message_id),
                                   caption= TEXT[user_lang]['user_profile']['step_3'],
                                   reply_markup = await get_gender_buttons(),
                                   parse_mode="HTML")


# выбор гендера
@dp.callback_query(F.data.in_([gender.value for gender in Gender]))
async def query_gender(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)

    # Преобразуем строку в Enum
    selected_gender = Gender(callback.data)

    # Сохраняем в базу (если update_user_fields поддерживает Enum)
    await update_user_fields(user_id, gender=selected_gender)

    # Получаем локализованную подпись
    gender_label = GENDER_LABELS[user_lang][selected_gender]

    # Уведомление
    await callback.answer(
        text=TEXT[user_lang]['notifications']['gender'].format(user_gender=gender_label)
    )

    # Переход к следующему шагу
    await callback.message.edit_caption(
        caption=TEXT[user_lang]['user_profile']['step_4'],
        reply_markup=await get_gender_search_buttons(),
        parse_mode="HTML"
    )


# выбора поиска: "Ищу Мужчину / Женщину / Пол не важен"
@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def query_gender_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)

    # Преобразуем в Gender Enum
    search_map = {
        "search_man": Gender.MAN,
        "search_woman": Gender.WOMAN,
        "search_any": Gender.ANY,
    }
    selected_gender_search = search_map[callback.data]

    # Обновляем в базе
    await update_user_fields(user_id, gender_search=selected_gender_search)

    # Получаем локализованную подпись
    label = GENDER_SEARCH_LABELS[user_lang][selected_gender_search]

    # Уведомление
    await callback.answer(
        text=TEXT[user_lang]['notifications']['gender_search'].format(gender_search=label)
    )

    # Переход к следующему шагу
    await callback.message.edit_caption(
        caption=TEXT[user_lang]['user_profile']['step_5'],
        reply_markup=None,
        parse_mode="HTML"
    )


# обработка фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(message)

    photo = message.photo[-1]
    file_id = photo.file_id
    
    user = await get_user_by_id(user_id)

    if not user.photo_id:
        await update_user_fields(user_id, photo_id = file_id) # запись в базу
        
        # изменяем запись
        start_message_id = await get_cached_message_id(user_id, "start_message_id")
        await bot.edit_message_caption(chat_id=message.chat.id,
                                    message_id=int(start_message_id),
                                    caption=TEXT[user_lang]['user_profile']['step_6'],
                                    parse_mode="HTML")
    else:
        print(file_id)

    await message.delete() # удаляем фото отправленное пользователем


# изменить анкету
@dp.callback_query(F.data == "profile_edit")
async def query_profile_edit(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_lang = await get_user_language(callback)

    # получаем id из Кэш и удаляем сообщение
    search_menu_message_id = await get_cached_message_id(user_id, "search_menu_message_id")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=search_menu_message_id)

    # получаем id из Кэш и удаляем сообщение
    match_menu_message_id = await get_cached_message_id(user_id, "match_menu_message_id")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=match_menu_message_id)

    start_message_id = await get_cached_message_id(user_id, "start_message_id")

    if not username:
        await bot.edit_message_caption(chat_id = callback.message.chat.id,
                                       message_id = int(start_message_id),
                                       caption = TEXT[user_lang]['user_profile']['username_error'],
                                       parse_mode ="HTML",
                                       reply_markup = await get_retry_registration_button())
        return
    
    # запись в базу
    await create_or_update_user(user_id, first_name, username)
    await update_user_fields(user_id, photo_id = None, about_me = None)

    await bot.edit_message_media(chat_id = callback.message.chat.id,
                                message_id = int(start_message_id),
                                media = InputMediaPhoto(media=USER_PROFILE_PICTURE))
    await bot.edit_message_caption(chat_id = callback.message.chat.id,
                                message_id = int(start_message_id),
                                caption = TEXT[user_lang]['user_profile']['step_1'].format(first_name=first_name),
                                parse_mode = "HTML",
                                reply_markup = await get_18yes_buttons())


# ------------------------------------------------------------------ Режим Инкогнито ----------------------------------------------------------


@dp.callback_query(F.data.startswith("incognito|"))
async def handle_incognito_toggle(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = await get_user_language(callback)
    _, action, _ = callback.data.split("|")

    user = await get_user_by_id(user_id)

    if action == "NOT_PAYED":

        prices = [LabeledPrice(label=f"Активировать режим Инкогнито", amount=PRICE_INCOGNITO)]

        sent_invoice = await callback.message.answer_invoice(
            title=f"Активировать режим Инкогнито",
            description=f"Купи один раз — и включай/выключай, когда хочешь!"
            "\nВ этом режиме тебя не видно в поиске, но ты можешь сам просматривать анкеты других.",
            payload=f"incognito_payment_ok|{PRICE_INCOGNITO}",
            provider_token="",
            currency="XTR",
            prices=prices,
            reply_markup=payment_keyboard()
        )

        # сохраняем в Кэш
        await save_to_cache(callback.from_user.id, "incognito_pay_message_id", message_id = sent_invoice.message_id)

        await callback.answer()
    else:
        if action == "ON":
            await update_user_fields(user_id, incognito_switch=False)
        else:
            await update_user_fields(user_id, incognito_switch=True)

    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await get_profile_edit_buttons(user.incognito_pay, user.incognito_switch))
    
    # двойное нажатие ??? но работает


# ------------------------------------------------------------------ ПОИСК ----------------------------------------------------------


# Колбек поиск вход
@dp.callback_query(F.data == "start_btn_search_menu")
async def btn_start_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    match = await find_first_matching_user(user_id)
    caption = await get_caption(match.first_name, match.country_local, match.city_local, match.about_me, match.gender, match.gender_search)

    if match:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=match.photo_id, caption=caption, parse_mode = "HTML"),
            reply_markup= await get_btn_to_search(match.first_name, match.telegram_id))
        await callback.answer()
    else:
        # TODO правильный ответ (изменить сообщение) + новая кнопка обновить
        await bot.send_message(user_id, "Пока никого не нашлось в вашем регионе 😔")


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

    photo_id, caption, markup = await get_btn_to_search()
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
    photo_id, caption, markup = await get_wants_user(reaction, PRICE_ADD_TO_MATCHES)
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, reply_markup=markup, parse_mode="HTML")


# ------------------------------------------------------------------- Оплата -------------------------------------------------------


# обработка колбека оплаты
@dp.callback_query(lambda c: c.data.startswith("wants_pay"))
async def handle_wants_pay(callback: types.CallbackQuery):
    _, target_tg_id, target_name, caption, photo_id, price_str, reaction = callback.data.split("|")
    price = int(price_str)

    prices = [LabeledPrice(label=f"Добавить {target_name} в Совпадения", amount=price)]

    sent_invoice = await callback.message.answer_invoice(
        title=f"Добавить в Совпадения {target_name}",
        description=f"При добавлении в Совпадения, вы получите доступ к профилю {target_name} и сможете ей/ему написать",
        payload=f"payment_ok|{target_tg_id}|{price}|{reaction}",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=payment_keyboard()
    )

    # сохраняем в Кэш
    await save_to_cache(callback.from_user.id, "invoice_message_id", message_id = sent_invoice.message_id)

    await callback.answer()


# ------------------------------------------------------------------- Оплата -------------------------------------------------------


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(lambda message: message.successful_payment is not None)
async def on_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id

    # Пример обработки payload:
    if payload.startswith("payment_ok"):
        _, target_id, price, reaction = payload.split("|")
        await add_payment(user_id, target_id, price) # запись в базу
        payment_message_id = await get_cached_message_id(user_id, "invoice_message_id")
    
        # изменяем запись
        user = await get_user_by_id(user_id)
        user_info = {"target_name": user.first_name, "caption": user.about_me, "photo_id": user.photo_id}
        markup = await get_wants_user(reaction, PRICE_ADD_TO_MATCHES, priced=True, user_info=user_info)

        match_menu_message_id = await get_cached_message_id(user_id, "match_menu_message_id")
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=int(match_menu_message_id), reply_markup=markup)

    elif payload.startswith("incognito_payment_ok"):
        # _, price = payload.split("|")
        await update_user_fields(user_id, incognito_pay=True, incognito_switch=True)
        payment_message_id = await get_cached_message_id(user_id, "incognito_pay_message_id")

        start_message_id = await get_cached_message_id(user_id, "start_message_id")
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=int(start_message_id), reply_markup=await get_profile_edit_buttons(True, True))

    # получаем id из Кэш и удаляем сообщение
    await bot.delete_message(chat_id=message.chat.id, message_id=payment_message_id)


# ------------------------------------------------------------------- Текст (Последний шаг в Анкете)-------------------------------------------------------


# обработка текста - добавляет или изменяет описание "о себе"
@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    user_lang = await get_user_language(message)
    start_message_id = await get_cached_message_id(user_id, "start_message_id")

    user = await get_user_by_id(user_id) # получение инфо о пользователе

    if not user.about_me:

        user_text = message.text
        if len(user_text) >= MIN_COUNT_SYMBOLS and len(user_text) <= MAX_COUNT_SYMBOLS:

            await update_user_fields(user_id, about_me = user_text) # запись в базу

            # изменяем запись
            await bot.edit_message_media(chat_id=message.chat.id,
                                        message_id=int(start_message_id),
                                        media=InputMediaPhoto(media=user.photo_id))
            await bot.edit_message_caption(chat_id=message.chat.id,
                                        message_id=int(start_message_id),
                                        reply_markup = await get_profile_edit_buttons(user.incognito_pay, user.incognito_switch),
                                        parse_mode="HTML",
                                        caption=TEXT[user_lang]["user_profile"]["profile"].format(first_name=user.first_name,
                                                                                                    country_local=user.country_local,
                                                                                                    city_local=user.city_local,
                                                                                                    gender=GENDER_LABELS[user_lang][user.gender],
                                                                                                    gender_search=GENDER_SEARCH_LABELS[user_lang][user.gender_search],
                                                                                                    about_me=user_text))

            match_menu = await message.answer_photo(photo=MATCH_MENU_PICTURE,
                                                    caption=TEXT[user_lang]['match_menu']['start'],
                                                    parse_mode="HTML",
                                                    reply_markup=await get_start_button_match_menu())
            # запись в базу
            await save_to_cache(user_id, "match_menu_message_id", message_id = match_menu.message_id)

            search_menu = await message.answer_photo(photo=SEARCH_MENU_PICTURE,
                                                    caption=TEXT[user_lang]['search_menu']['start'],
                                                    parse_mode="HTML",
                                                    reply_markup=await get_start_button_search_menu())
            # запись в базу
            await save_to_cache(user_id, "search_menu_message_id", message_id = search_menu.message_id)


        elif len(user_text) < MIN_COUNT_SYMBOLS:
            await bot.edit_message_caption(chat_id=message.chat.id,
                                message_id=int(start_message_id),
                                caption=TEXT[user_lang]['user_profile']['min_count_symbols_error'].format(MIN_COUNT_SYMBOLS=MIN_COUNT_SYMBOLS, text_length=len(user_text)),
                                reply_markup = None,
                                parse_mode="HTML")
        elif len(user_text) > MAX_COUNT_SYMBOLS:
            await bot.edit_message_caption(chat_id=message.chat.id,
                                message_id=int(start_message_id),
                                caption=TEXT[user_lang]['user_profile']['max_count_symbols_error'].format(MAX_COUNT_SYMBOLS=MAX_COUNT_SYMBOLS, text_length=len(user_text)),
                                reply_markup = None,
                                parse_mode="HTML")
    
    await message.delete() # удаляем сообщение пользователя


# ------------------------------------------------------------------- Обработка других форматов -------------------------------------------------------


# TODO обработка других типов и форматов, удалять все из чата
@dp.message(~(F.text | F.photo | F.location))
async def delete_unwanted(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"⚠️ Не удалось удалить сообщение: {e}")


# ------------------------------------------------------------------- Активация бота -------------------------------------------------------


async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())