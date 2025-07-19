import logging
import aiohttp
import asyncio
from db_connect import async_engine
from aiogram.types import InputMediaPhoto, LabeledPrice
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import *
from models import ReactionType, Gender, Base, PaymentType
from buttons import *
from functions import *
from languages import get_texts


# ------------------------------------------------------------------- Настройка бота -------------------------------------------------------


# TODO Supabase - SQL bd Postgres
# Локализация
# Меню совпадений
# intent - Название? dating_good_bot Twint - Twin + Intent — совпадение намерений Intendy	Intent + -y = дружелюбно


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
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)

    await message.delete() #удалить сообщение пользователя /start

    if not username:
        starting_message = await message.answer_photo(photo=NO_USERNAME_PICTURE,
                                   caption=texts["TEXT"]['user_profile']['username_error'],
                                   parse_mode="HTML",
                                   reply_markup=await get_retry_registration_button())
        
        await save_to_cache(user_id, "start_message_id", message_id = starting_message.message_id) # запись в базу
        return
               
    await create_or_update_user(user_id, first_name, username)  # запись в базу

    user = await get_user_by_id(user_id)

    if user.about_me:
        starting_message = await message.answer_photo(photo=user.photo_id,
                                                      parse_mode="HTML",
                                                      reply_markup=await get_profile_edit_buttons(user.incognito_pay, user.incognito_switch),
                                                      caption=texts["TEXT"]["user_profile"]["profile"].format(first_name=user.first_name,
                                                                                                                country_local=user.country_local,
                                                                                                                city_local=user.city_local,
                                                                                                                gender=texts['GENDER_LABELS'][user.gender],
                                                                                                                gender_search=texts['GENDER_SEARCH_LABELS'][user.gender_search],
                                                                                                                about_me=user.about_me))
                                                                                                                
        match_menu = await message.answer_photo(photo=MATCH_MENU_PICTURE,
                                                caption=texts['TEXT']['match_menu']['start'],
                                                parse_mode="HTML",
                                                reply_markup=await get_start_button_match_menu())
        
        await save_to_cache(user_id, "match_menu_message_id", message_id = match_menu.message_id) # запись в базу

        search_menu = await message.answer_photo(photo=SEARCH_MENU_PICTURE,
                                                caption=texts['TEXT']['search_menu']['start'],
                                                parse_mode="HTML",
                                                reply_markup=await get_start_button_search_menu())
        
        await save_to_cache(user_id, "search_menu_message_id", message_id = search_menu.message_id) # запись в базу

    else:
        starting_message = await message.answer_photo(photo=USER_PROFILE_PICTURE,
                                                      caption=texts['TEXT']['user_profile']['step_1'].format(first_name=first_name, notion_site=NOTION_SITE),
                                                      parse_mode="HTML",
                                                      reply_markup=await get_approval_button())
    # запись в базу
    await save_to_cache(user_id, "start_message_id", message_id = starting_message.message_id)


# повторная регистрация, если нет username
@dp.callback_query(F.data == "retry_registration")
async def query_retry_registration(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    if not username:
        return
    
    # запись в базу
    await create_or_update_user(user_id, first_name, username)
    
    # изменяем стартовую запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=int(start_message_id),
        media=InputMediaPhoto(
            media=USER_PROFILE_PICTURE,
            caption=texts['TEXT']['user_profile']['step_1'].format(first_name=first_name, notion_site=NOTION_SITE),
            parse_mode="HTML"),
        reply_markup=await get_approval_button())


# подтверждение 18 лет
@dp.callback_query(F.data == "18yes_and_approval")
async def query_18years(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    # запись в базу
    await update_user_fields(user_id, eighteen_years_and_approval=True)

    # уведомление сверху
    await callback.answer(text=texts['TEXT']['notifications']['18year'])

    # 1. Меняем текст сообщения и убираем inline-кнопки
    await callback.message.edit_caption(caption=texts['TEXT']['user_profile']['step_2'], parse_mode="HTML", reply_markup=None)

    # 2. Отдельно отправляем сообщение с обычной клавиатурой для геолокации
    location_message = await callback.message.answer(texts['TEXT']['user_profile']['get_location_message'],
                                                     reply_markup= await get_location_button(), parse_mode="HTML")
    
    # запись в базу
    await save_to_cache(user_id, "location_message_id", message_id = location_message.message_id)


# TODO - тормозит await asyncio.gather(*tasks)

# подтверждение локации
@dp.message(F.location)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)

    user = await get_user_by_id(user_id)

    await message.delete() #удалить сообщение пользователя с локацией

    #защита от повторного ввода, удаление сообщения с локацией
    if user.city or user.country:
        return

    latitude = message.location.latitude
    longitude = message.location.longitude

    user_language_code = message.from_user.language_code or 'en'

    if user_language_code == 'en':
        country_en, city_en = await get_location_opencage(latitude, longitude, lang='en')
        country_local, city_local = country_en, city_en
    else:
        # Запускаем сразу два запроса параллельно
        (country_local, city_local), (country_en, city_en) = await asyncio.gather(
            get_location_opencage(latitude, longitude, lang=user_language_code),
            get_location_opencage(latitude, longitude, lang='en')
        )

    # запись в базу
    await update_user_fields(user_id, country=country_en, city=city_en, country_local=country_local, city_local=city_local)

    # получаем id из Кэш и удаляем сообщение
    location_message_id = await get_cached_message_id(user_id, "location_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=location_message_id)

    # изменяем запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")
    await bot.edit_message_caption(chat_id=message.chat.id,
                                   message_id=int(start_message_id),
                                   caption= texts['TEXT']['user_profile']['step_3'],
                                   reply_markup = await get_gender_buttons(),
                                   parse_mode="HTML")


# выбор гендера
@dp.callback_query(F.data.in_([gender.value for gender in Gender]))
async def query_gender(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    # Преобразуем строку в Enum
    selected_gender = Gender(callback.data)

    # Сохраняем в базу (если update_user_fields поддерживает Enum)
    await update_user_fields(user_id, gender=selected_gender)

    # Получаем локализованную подпись
    gender_label = texts['GENDER_LABELS'][selected_gender]

    # Уведомление
    await callback.answer(
        text=texts['TEXT']['notifications']['gender'].format(user_gender=gender_label)
    )

    # Переход к следующему шагу
    await callback.message.edit_caption(
        caption=texts['TEXT']['user_profile']['step_4'],
        reply_markup=await get_gender_search_buttons(),
        parse_mode="HTML"
    )


# выбора поиска: "Ищу Мужчину / Женщину / Пол не важен"
@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def query_gender_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

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
    label = texts['GENDER_SEARCH_LABELS'][selected_gender_search]

    # Уведомление
    await callback.answer(
        text=texts['TEXT']['notifications']['gender_search'].format(gender_search=label)
    )

    # Переход к следующему шагу
    await callback.message.edit_caption(
        caption=texts['TEXT']['user_profile']['step_5'],
        reply_markup=None,
        parse_mode="HTML"
    )


# обработка фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)

    photo = message.photo[-1]
    file_id = photo.file_id
    
    user = await get_user_by_id(user_id)

    # защита от повторов, удаляем фото
    if user.photo_id:
        print(file_id)
        await message.delete()
        return

    await update_user_fields(user_id, photo_id = file_id) # запись в базу
    
    # изменяем запись
    start_message_id = await get_cached_message_id(user_id, "start_message_id")
    await bot.edit_message_caption(chat_id=message.chat.id,
                                message_id=int(start_message_id),
                                caption=texts['TEXT']['user_profile']['step_6'],
                                parse_mode="HTML")

    await message.delete() # удаляем фото отправленное пользователем


# изменить анкету
@dp.callback_query(F.data == "profile_edit")
async def query_profile_edit(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

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
                                       caption = texts['TEXT']['user_profile']['username_error'],
                                       parse_mode ="HTML",
                                       reply_markup = await get_retry_registration_button())
        return
    
    # запись в базу
    await create_or_update_user(user_id, first_name, username)
    await update_user_fields(user_id, **{k: None for k in ["gender", "gender_seach", "country", "country_local", "city", "city_local", "photo_id", "about_me"]})

    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=int(start_message_id),
        media=InputMediaPhoto(
            media=USER_PROFILE_PICTURE,
            caption=texts['TEXT']['user_profile']['step_1'].format(first_name=first_name, notion_site=NOTION_SITE),
            parse_mode="HTML"),
        reply_markup=await get_approval_button())


# ------------------------------------------------------------------ Режим Инкогнито ----------------------------------------------------------


@dp.callback_query(F.data.startswith("incognito|"))
async def handle_incognito_toggle(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)
    _, action, _ = callback.data.split("|")

    user = await get_user_by_id(user_id)

    label = texts['TEXT']["payment"]["incognito"]["lable"]
    title = texts['TEXT']["payment"]["incognito"]["title"]
    description = texts['TEXT']["payment"]["incognito"]["description"]

    if action == "NOT_PAYED":

        prices = [LabeledPrice(label=label, amount=PRICE_INCOGNITO)]

        sent_invoice = await callback.message.answer_invoice(
            title=title,
            description=description,
            payload=f"payment_incognito|{PRICE_INCOGNITO}",
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


# ------------------------------------------------------------------- Удаление аккаунта -------------------------------------------------------


# Команда Удаление
@dp.message(Command("delete_profile"))
async def cmd_delete_profile(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    search_menu_message_id = await get_cached_message_id(user_id, "search_menu_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=int(search_menu_message_id))

    match_menu_message_id = await get_cached_message_id(user_id, "match_menu_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=int(match_menu_message_id))

    start_message_id = await get_cached_message_id(user_id, "start_message_id")
    await bot.delete_message(chat_id=message.chat.id, message_id=int(start_message_id))

    await message.delete()

    await delete_user_by_id(user_id)


# ------------------------------------------------------------------- Бан аккаунта -------------------------------------------------------


# ------------------------------------------------------------------ ПОИСК ----------------------------------------------------------


# колбек поиск вход
@dp.callback_query(F.data == "start_btn_search_menu")
async def btn_start_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    target_user = await find_first_matching_user(user_id) # поиск
    
    if target_user:
        caption = await get_caption(target_user)
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=target_user.photo_id, caption=caption, parse_mode = "HTML"),
            reply_markup = await get_btn_to_search(target_user.first_name, target_user.telegram_id))
    else:
        caption = texts['TEXT']["search"]["not_found"]
        notification = texts['TEXT']["notifications"]["not_found"]
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=NOT_FOUND_PICTURE, caption=caption, parse_mode = "HTML"),
            reply_markup = await reload_search())
        await callback.answer(notification) # уведомление сверху


# обработка колбека реакции
@dp.callback_query(lambda c: c.data.startswith("reaction"))
async def handle_reaction(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    _, reaction_str, target_name, target_tg_id = callback.data.split("|", 3)

    await add_reaction(user_id, target_tg_id, reaction_str) # запись в базу
    
    reaction = ReactionType(reaction_str)
    await callback.answer(reaction.message_template.format(name=target_name)) # уведомление сверху

    target_user = await find_first_matching_user(user_id) # поиск

    if target_user:
        caption = await get_caption(target_user)
        markup = await get_btn_to_search(target_user.first_name, target_user.telegram_id)
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=target_user.photo_id, caption=caption, parse_mode = "HTML"),
            reply_markup = markup)
    else:
        caption = texts['TEXT']["search"]["not_found"]
        notification = texts['TEXT']["notifications"]["not_found"]
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=NOT_FOUND_PICTURE, caption=caption, parse_mode = "HTML"),
            reply_markup = await reload_search())
        await callback.answer(notification) # уведомление сверху


# колбек повторить поиск
@dp.callback_query(F.data == "reload_search")
async def btn_reload_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    target_user = await find_first_matching_user(user_id) # поиск
    
    if target_user:
        caption = await get_caption(target_user)
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=target_user.photo_id, caption=caption, parse_mode = "HTML"),
            reply_markup = await get_btn_to_search(target_user.first_name, target_user.telegram_id))
    else:
        await callback.answer(texts['TEXT']["notifications"]["not_found"]) # уведомление сверху


# ------------------------------------------------------------------ СОВПАДЕНИЯ ----------------------------------------------------------


# колбек кнопка старт у меню совпадений
@dp.callback_query(lambda c: c.data.startswith("start_btn_match_menu"))
async def query_start__reload_btn_match_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    # Параллельный запуск всех функций
    results = await asyncio.gather(
        get_match_targets(user_id),
        get_collection_targets(user_id),
        get_intent_targets(user_id, "LOVE"),
        get_intent_targets(user_id, "SEX"),
        get_intent_targets(user_id, "CHAT"),
    )

    # Распаковка результатов
    (_, match_count), (_, collection_count), (_, love_count), (_, sex_count), (_, chat_count) = results

    markup = await get_matches_menu_buttons(match_count, collection_count, love_count, sex_count, chat_count)

    await callback.message.edit_media(media=InputMediaPhoto(media=MATCH_MENU_PICTURE,
                                                            caption=texts['TEXT']['match_menu']['start'],
                                                            parse_mode = "HTML"),
                                    reply_markup = markup)

    # await callback.message.edit_reply_markup(reply_markup=markup)
    await callback.answer(texts['TEXT']["notifications"]["reloaded"]) # уведомление сверху


# колбек кнопка мэтчи в меню Совпадений
@dp.callback_query(F.data == "matches")
async def query_matches(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    target_users_ids, _ = await get_match_targets(user_id)

    if not target_users_ids:
        photo_id = MATCH_MENU_PICTURE
        caption = texts['TEXT']['match_menu']['start']
        markup = await empty_category_buttons()
    else:
        target_user = await get_user_by_id(target_users_ids[0])
        prev_id, next_id = await get_prev_next_ids(target_users_ids[0], target_users_ids)
        photo_id = target_user.photo_id
        caption = await get_caption(target_user)
        markup = await get_matches_user(target_user, [prev_id, next_id])

    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption, parse_mode = "HTML"),
                                      reply_markup = markup)


# вперед/назад при навигации у меню Совпадений
@dp.callback_query(lambda c: c.data.startswith("matches_navigation"))
async def query_matches_navigation(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    _, target_id = callback.data.split("|", 1)

    if target_id == 'pass':
        await callback.answer(texts['TEXT']["notifications"]["empty"]) # уведомление сверху
        return

    target_id = int(target_id)
    target_users_ids, _ = await get_match_targets(user_id)
    prev_id, next_id = await get_prev_next_ids(target_id, target_users_ids)

    target_user = await get_user_by_id(target_id)
    photo_id = target_user.photo_id
    caption = await get_caption(target_user)
    markup = await get_matches_user(target_user, [prev_id, next_id])

    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption, parse_mode = "HTML"),
                                      reply_markup = markup)


# колбека кому нравишься
@dp.callback_query(lambda c: c.data.startswith("who_wants"))
async def handle_who_wants(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, reaction = callback.data.split("|", 1)
    photo_id, caption, markup = await get_wants_user(reaction, PRICE_ADD_TO_MATCHES)
    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id))
    await callback.message.edit_caption(caption=caption, reply_markup=markup, parse_mode="HTML")


# обработка колбека оплаты
@dp.callback_query(lambda c: c.data.startswith("wants_pay"))
async def handle_wants_pay(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    _, target_tg_id, target_name, caption, photo_id, price_str, reaction = callback.data.split("|")
    price = int(price_str)

    label = texts["TEXT"]["payment"]["collection"]["label"]
    title = texts["TEXT"]["payment"]["collection"]["title"]
    description = texts["TEXT"]["payment"]["collection"]["description"]

    prices = [LabeledPrice(label=label.format(target_name=target_name), amount=price)] #🏆 💫 ⭐ Избранное

    sent_invoice = await callback.message.answer_invoice(
        title=title.format(target_name=target_name),
        description=description.format(target_name=target_name),
        payload=f"payment_add_to_collection|{target_tg_id}|{price}|{reaction}",
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

    if payload.startswith("payment_add_to_collection"):
        _, target_id, amount, reaction = payload.split("|")

        await add_payment(user_id, amount, PaymentType.COLLECTION, target_id) # запись в базу

        payment_message_id = await get_cached_message_id(user_id, "invoice_message_id")
    
        # изменяем запись
        target_id = await get_user_by_id(target_id)
        user_info = {"target_name": target_id.first_name, "caption": target_id.about_me, "photo_id": target_id.photo_id}
        markup = await get_wants_user(reaction, PRICE_ADD_TO_MATCHES, priced=True, user_info=user_info)

        match_menu_message_id = await get_cached_message_id(user_id, "match_menu_message_id")
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=int(match_menu_message_id), reply_markup=markup)

    elif payload.startswith("payment_incognito"):
        _, amount = payload.split("|")
        await add_payment(user_id, amount, PaymentType.INCOGNITO) # запись в базу

        await update_user_fields(user_id, incognito_pay=True, incognito_switch=True) # запись в базу

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
    user_lang = message.from_user.language_code
    texts = await get_texts(user_lang)

    start_message_id = await get_cached_message_id(user_id, "start_message_id")

    user = await get_user_by_id(user_id) # получение инфо о пользователе

    # защита от повторов, удаление текста
    if user.about_me:
        await message.delete() 
        return

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
                                    caption=texts['TEXT']["user_profile"]["profile"].format(first_name=user.first_name,
                                                                                                country_local=user.country_local,
                                                                                                city_local=user.city_local,
                                                                                                gender=texts['GENDER_LABELS'][user.gender],
                                                                                                gender_search=texts['GENDER_SEARCH_LABELS'][user.gender_search],
                                                                                                about_me=user_text))

        match_menu = await message.answer_photo(photo=MATCH_MENU_PICTURE,
                                                caption=texts['TEXT']['match_menu']['start'],
                                                parse_mode="HTML",
                                                reply_markup=await get_start_button_match_menu())
        # запись в базу
        await save_to_cache(user_id, "match_menu_message_id", message_id = match_menu.message_id)

        search_menu = await message.answer_photo(photo=SEARCH_MENU_PICTURE,
                                                caption=texts['TEXT']['search_menu']['start'],
                                                parse_mode="HTML",
                                                reply_markup=await get_start_button_search_menu())
        # запись в базу
        await save_to_cache(user_id, "search_menu_message_id", message_id = search_menu.message_id)


    elif len(user_text) < MIN_COUNT_SYMBOLS:
        await bot.edit_message_caption(chat_id=message.chat.id,
                            message_id=int(start_message_id),
                            caption=texts['TEXT']['user_profile']['min_count_symbols_error'].format(MIN_COUNT_SYMBOLS=MIN_COUNT_SYMBOLS, text_length=len(user_text)),
                            reply_markup = None,
                            parse_mode="HTML")
    elif len(user_text) > MAX_COUNT_SYMBOLS:
        await bot.edit_message_caption(chat_id=message.chat.id,
                            message_id=int(start_message_id),
                            caption=texts['TEXT']['user_profile']['max_count_symbols_error'].format(MAX_COUNT_SYMBOLS=MAX_COUNT_SYMBOLS, text_length=len(user_text)),
                            reply_markup = None,
                            parse_mode="HTML")
    
    await message.delete() # удаляем сообщение пользователя


# ------------------------------------------------------------------- Обработка других форматов -------------------------------------------------------


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