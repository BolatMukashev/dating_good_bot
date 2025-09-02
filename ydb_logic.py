import logging
import asyncio
from aiogram.types import InputMediaPhoto, LabeledPrice
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from config import *
from buttons import *
from postgresql_functions import *
from languages import get_texts
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from datetime import datetime
from languages.desc import DESCRIPTIONS, SHORT_DESCRIPTIONS, NAMES
from ydb_functions import *


# ------------------------------------------------------------------- Настройка -------------------------------------------------------

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ------------------------------------------------------------------- ТЕСТ ЗАПУСК -------------------------------------------------------


# # Команда Старт
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("hello")


# # обработка фото
# @dp.message(F.photo)
# async def handle_photo(message: types.Message):
#     photo = message.photo[-1]
#     file_id = photo.file_id

#     await message.answer(f"{file_id}")

# ------------------------------------------------------------------- АНКЕТА -------------------------------------------------------


# Команда Старт
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    first_name = message.from_user.first_name
    username = message.from_user.username

    # print(user_lang)

    # получение текста на языке пользователя и удаление сообщения /start
    texts = await get_texts(user_lang)
    await message.delete()

    if not username:
        picture = Pictures.NO_USERNAME_PICTURE.value
        caption = texts["TEXT"]['user_profile']['username_error']
        markup = await get_retry_registration_button(texts)

    else:

        # получение и обновление инфо о пользователе
        async with UserClient() as client:
            new_user = User(telegram_id=user_id, first_name=first_name, username=username)
            user = await client.insert_user(new_user)

        if user.about_me:
            picture = user.photo_id
            markup = await get_profile_edit_buttons(user.incognito_pay, user.incognito_switch, texts)
            caption = texts["TEXT"]["user_profile"]["profile"].format(first_name=user.first_name,
                                                                        country_local=user.country_local,
                                                                        city_local=user.city_local,
                                                                        gender=texts['GENDER_LABELS'][user.gender],
                                                                        gender_emoji=texts['GENDER_EMOJI'][user.gender],
                                                                        gender_search=texts['GENDER_SEARCH_LABELS'][user.gender_search],
                                                                        about_me=user.about_me)
        else:
            picture = Pictures.USER_PROFILE_PICTURE.value
            caption = texts['TEXT']['user_profile']['step_1'].format(first_name=first_name, notion_site=NOTION_SITE)
            markup = await get_approval_button(texts)

    starting_message = await message.answer_photo(photo=picture, caption=caption, reply_markup=markup)
    async with CacheClient() as cache_client:
        new_cache = Cache(telegram_id=user_id, parameter="start_message_id", message_id=starting_message.message_id)
        await cache_client.insert_cache(new_cache)

    # если уже зарегистрирован в базе
    if user.about_me and username:

        match_menu = await message.answer_photo(photo=Pictures.MATCH_MENU_PICTURE.value,
                                                caption=texts['TEXT']['match_menu']['start'],
                                                reply_markup=await get_start_button_match_menu(texts))

        search_menu = await message.answer_photo(photo=Pictures.SEARCH_MENU_PICTURE.value,
                                                caption=texts['TEXT']['search_menu']['start'],
                                                reply_markup=await get_start_button_search_menu(texts))
        # запись в базу
        async with CacheClient() as cache_client:
            new_cache1 = Cache(telegram_id=user_id, parameter="match_menu_message_id", message_id=match_menu.message_id)
            new_cache2 = Cache(telegram_id=user_id, parameter="search_menu_message_id", message_id=search_menu.message_id)
            await asyncio.gather(
                await cache_client.insert_cache(new_cache1),
                await cache_client.insert_cache(new_cache2)
            )


# повторная регистрация, если нет username
@dp.callback_query(F.data == "retry_registration")
async def query_retry_registration(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_lang = callback.from_user.language_code
    
    if not username:
        return
    
    # получаем id стартового сообщения, обновляем инфу о пользователе, получаем текст на языке пользователя
    async with CacheClient() as cache_client, UserClient() as user_client:
        cached_messages, texts, _ = await asyncio.gather(
            cache_client.get_cache_by_telegram_id(user_id),
            get_texts(user_lang),
            user_client.insert_user(
                User(telegram_id=user_id, first_name=first_name, username=username)
            )
        )

    # изменяем стартовое сообщение
    await bot.edit_message_media(
        chat_id = callback.message.chat.id,
        message_id = cached_messages.get("start_message_id"),
        media = InputMediaPhoto(media = Pictures.USER_PROFILE_PICTURE.value,
                                caption = texts['TEXT']['user_profile']['step_1'].format(first_name=first_name, notion_site=NOTION_SITE)),
        reply_markup = await get_approval_button(texts))


# подтверждение 18 лет
@dp.callback_query(F.data == "18yes_and_approval")
async def query_18years(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code

    # получаем язык пользователя, обновляем инфо о пользователе в базе
    async with UserClient() as client:
        texts, _ = await asyncio.gather(
            get_texts(user_lang),
            client.update_user_fields(user_id, eighteen_years_and_approval=True)
        )

    # кидаем уведомление, меняем стартовое сообщение
    await callback.answer(text=texts['TEXT']['notifications']['18year'])
    await callback.message.edit_caption(caption=texts['TEXT']['user_profile']['step_2'], reply_markup=None)

    # отдельно отправляем сообщение с обычной клавиатурой для геолокации
    location_message = await callback.message.answer(texts['TEXT']['user_profile']['get_location_message'],
                                                     reply_markup= await get_location_button(texts))
    
    async with CacheClient() as cache_client:
        new_cache = Cache(telegram_id=user_id, parameter="location_message_id", message_id=location_message.message_id)
        await cache_client.insert_cache(new_cache)


# подтверждение локации
@dp.message(F.location)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    latitude = message.location.latitude
    longitude = message.location.longitude

    # получение инфо о пользователе, получение текста на языке пользователя, удаление сообщения с локацией
    async with UserClient() as user_client:
        user, texts = await asyncio.gather(
            user_client.get_user_by_id(user_id),
            get_texts(user_lang)
        )

    await message.delete()

    #защита от повторного ввода
    if user.city or user.country:
        return

    if user_lang == 'en':
        country_en, city_en = await get_location_opencage(latitude, longitude, lang='en')
        country_local, city_local = country_en, city_en
    else:
        # Запускаем сразу два запроса параллельно
        (country_local, city_local), (country_en, city_en) = await asyncio.gather(
            get_location_opencage(latitude, longitude, lang=user_lang),
            get_location_opencage(latitude, longitude, lang='en')
        )

   # Получаем message_id из кэш
    async with CacheClient() as cache_client:
        cached_messages = await cache_client.get_cache_by_telegram_id(user_id)
        start_message_id = cached_messages.get("start_message_id")

    # обновляем инфо о пользователе, удаляем кэш
    async with UserClient() as user_client, CacheClient() as cache_client:
        await asyncio.gather(
            user_client.update_user_fields(user_id, country=country_en, city=city_en, country_local=country_local, city_local=city_local),
            cache_client.delete_cache_by_telegram_id_and_parameter(user_id, "location_message_id")
        )

    # удаляем сообщение о геолокации, изменяем стартовое сообщение
    await bot.delete_message(chat_id=message.chat.id, message_id=cached_messages.get("location_message_id"))
    await bot.edit_message_caption(
            chat_id = message.chat.id,
            message_id = start_message_id,
            caption = texts['TEXT']['user_profile']['step_3'],
            reply_markup = await get_gender_buttons(texts)
        )


# выбор гендера
@dp.callback_query(F.data.in_([gender.value for gender in Gender]))
async def query_gender(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code

    selected_gender = Gender(callback.data) # Преобразуем строку в Enum

    # получение текста на языке пользователя, обновление инфо о пользователе
    async with UserClient() as user_client:
        texts, _ = await asyncio.gather(
            get_texts(user_lang),
            user_client.update_user_fields(user_id, gender=selected_gender)
        )

    # получаем локализованную подпись
    gender_label = texts['GENDER_LABELS'][selected_gender]

    # уведомление и переход к следующему шагу
    await callback.answer(text=texts['TEXT']['notifications']['gender'].format(user_gender=gender_label))
    await callback.message.edit_caption(caption=texts['TEXT']['user_profile']['step_4'],
                                      reply_markup=await get_gender_search_buttons(texts))


# выбора поиска: "Ищу Мужчину / Женщину / Пол не важен"
@dp.callback_query(F.data.in_(["search_man", "search_woman", "search_any"]))
async def query_gender_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    
    # преобразуем в Gender Enum
    search_map = {
        "search_man": Gender.MAN,
        "search_woman": Gender.WOMAN,
        "search_any": Gender.ANY,
    }
    selected_gender_search = search_map[callback.data]

    # получаем текст на языке пользователя, обновляем в базе инфо о пользователе
    async with UserClient() as user_client:
        texts, _ = await asyncio.gather(
            get_texts(user_lang),
            user_client.update_user_fields(user_id, gender_search=selected_gender_search)
        )

    # Уведомление и переход к следующему шагу
    await callback.answer(text=texts['TEXT']['notifications']['gender_search'].format(gender_search=texts['GENDER_SEARCH_LABELS'][selected_gender_search]))
    await callback.message.edit_caption(caption=texts['TEXT']['user_profile']['step_5'], reply_markup=None)


# обработка фото
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code
    photo = message.photo[-1]
    file_id = photo.file_id

    # получение инфо о пользователе, получение текста на языке пользователя, удаление сообщения с фото
    async with UserClient() as user_client:
        user, texts = await asyncio.gather(
            user_client.get_user_by_id(user_id),
            get_texts(user_lang)
        )

    await message.delete()

    # защита от повторов, удаляем фото
    if user.photo_id or not user.gender_search:
        print(file_id)
        return
    
    # получение id стартового сообщения, обновление инфо о пользователе
    async with UserClient() as user_client, CacheClient() as cache_client:
        cached_messages, _ = await asyncio.gather(
            cache_client.get_cache_by_telegram_id(user_id),
            user_client.update_user_fields(user_id, photo_id = file_id)
        )

    await bot.edit_message_caption(chat_id=message.chat.id,
                                   message_id=cached_messages.get("start_message_id"),
                                   caption=texts['TEXT']['user_profile']['step_6'])


# ------------------------------------------------------------------ ИЗМЕНЕНИЕ АНКЕТЫ ----------------------------------------------------------


# изменить анкету
@dp.callback_query(F.data == "profile_edit")
async def query_profile_edit(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_lang = callback.from_user.language_code

    # получаем id сообщений из кэша и текст на языке пользователя
    async with CacheClient() as cache_client:
        cached_messages, texts = await asyncio.gather(
            cache_client.get_cache_by_telegram_id(user_id),
            get_texts(user_lang)
        )

    start_message_id = cached_messages.get("start_message_id")

    # пары параметр → id сообщения
    messages_to_delete = {
        "match_menu_message_id": cached_messages.get("match_menu_message_id"),
        "search_menu_message_id": cached_messages.get("search_menu_message_id"),
    }

    # удаляем или блокируем меню мэтч и меню поиска 
    for parameter, message_id in messages_to_delete.items():
        if not message_id:
            continue
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=message_id)
        except TelegramBadRequest as e:
            print(f"ошибка удаления сообщений: {e}")
            try:
                await bot.edit_message_media(chat_id=callback.message.chat.id,
                                             message_id=message_id,
                                             media=InputMediaPhoto(media=Pictures.CLEANING.value,
                                                                   caption=texts['TEXT']['user_profile']['waiting'])
                                            )
            except Exception as e:
                print(f"ошибка изменения сообщений: {e}")
        else:
            # теперь удаляем из кэша по telegram_id + parameter
            async with CacheClient() as cache_client:
                await cache_client.delete_cache_by_telegram_id_and_parameter(user_id, parameter)
            
    # изменение стартового сообщения
    if not username:
        caption = texts['TEXT']['user_profile']['username_error']
        markup = await get_retry_registration_button(texts)
    else:
        caption = texts['TEXT']['user_profile']['step_1'].format(first_name=first_name, notion_site=NOTION_SITE)
        markup = await get_approval_button(texts)
    
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=start_message_id,
                                 media=InputMediaPhoto(media=Pictures.USER_PROFILE_PICTURE.value,
                                                       caption=caption),
                                 reply_markup=markup)
    
    # обновляем инфо о пользователе, удаляем записи по остальным полям в бд
    async with UserClient() as user_client:
        user = await user_client.get_user_by_id(user_id)
        empty_user = User(telegram_id = user_id,
                          first_name = first_name,
                          username = username,
                          gender= None,
                          gender_search= None,
                          country= None,
                          city= None,
                          country_local= None,
                          city_local= None,
                          photo_id=None,
                          about_me=None,
                          incognito_pay = user.incognito_pay,
                          incognito_switch = user.incognito_switch,
                          banned = user.banned)
        await user_client.insert_user(empty_user)


# ------------------------------------------------------------------ ИНКОГНИТО ----------------------------------------------------------


@dp.callback_query(F.data.startswith("incognito|"))
async def handle_incognito_toggle(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code

    texts = await get_texts(user_lang)

    _, action, _ = callback.data.split("|")

    # если НЕ ОПЛАЧЕНО, отправка оплаты
    if action == "NOT_PAYED":

        amount = (PRICES.get(user_lang) or PRICES["en"]).get("incognito")

        label = texts['TEXT']["payment"]["incognito"]["label"]
        title = texts['TEXT']["payment"]["incognito"]["title"]
        description = texts['TEXT']["payment"]["incognito"]["description"]
        prices = [LabeledPrice(label=label, amount=amount)]

        # получение id сообщений
        async with CacheClient() as cache_client:
            cached_messages = await cache_client.get_cache_by_telegram_id(user_id)
        pay_message_id = cached_messages.get('incognito_pay_message_id')
        if pay_message_id:
            try:
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=pay_message_id)
            except TelegramBadRequest as e:
                print(f"ошибка удаления сообщений: {e}")

        sent_invoice = await callback.message.answer_invoice(
            title=title,
            description=description,
            payload=f"payment_incognito|{amount}",
            provider_token="",
            currency="XTR",
            prices=prices,
            reply_markup=payment_keyboard(texts)
        )
        async with CacheClient() as cache_client:
            new_cache = Cache(telegram_id=user_id, parameter="incognito_pay_message_id", message_id=sent_invoice.message_id)
            await cache_client.insert_cache(new_cache)

        await callback.answer(texts["TEXT"]["notifications"]["payment_sent"])

    else:
        # получение инфо о пользователе и изменение статуса в бд
        async with UserClient() as user_client:
            user = await user_client.get_user_by_id(user_id)
            if action == "ON":
                await user_client.update_user_fields(user_id, incognito_switch=False)
            else:
                await user_client.update_user_fields(user_id, incognito_switch=True)

    # изменение клавиатуры у стартового сообщения, отправка уведомления
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=await get_profile_edit_buttons(user.incognito_pay, user.incognito_switch, texts))
    await callback.answer(texts["TEXT"]["notifications"]["incognito"][user.incognito_switch])


# ------------------------------------------------------------------- Удаление аккаунта -------------------------------------------------------


# Команда Удаление
@dp.message(Command("delete_profile"))
async def cmd_delete_profile(message: types.message):
    user_id = message.from_user.id

    # получение id сообщений
    async with CacheClient() as cache_client:
        cached_messages = await cache_client.get_cache_by_telegram_id(user_id)

    message_ids = ["start_message_id", "match_menu_message_id", "search_menu_message_id"]

    # удаление сообщений и пользователя из базы
    for el in message_ids:
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=cached_messages.get(el))
        except TelegramBadRequest as e:
            print(f"ошибка удаления сообщений: {e}")
        
    async with CacheClient() as cache_client, UserClient() as user_client:
        await cache_client.delete_cache_by_telegram_id(user_id)
        await user_client.delete_user(user_id)
        
    await message.delete()


# ------------------------------------------------------------------- Бан аккаунта -------------------------------------------------------


# ------------------------------------------------------------------- Тест API Telegram -------------------------------------------------------


# отправка тестового сообщения
@dp.message(Command("test"))
async def cmd_delete_msg(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        msg = await message.answer_photo(photo=Pictures.TECHNICAL_WORK.value, caption="Тестовое сообщение")
    
    async with CacheClient() as cache_client:
        new_cache = Cache(telegram_id=user_id, parameter="test_message_id", message_id=msg.message_id)
        await cache_client.insert_cache(new_cache)
    
    await message.delete()


# проверка удаления сообщения (после 2 суток простоя)
@dp.message(Command("test1"))
async def cmd_delete_msg1(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        async with CacheClient() as cache_client:
             cached_messages = await cache_client.get_cache_by_telegram_id(user_id)

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=cached_messages.get("test_message_id"))
        except TelegramBadRequest as e:
            print(f"ошибка удаления: {e}")
    
    await message.delete()


# проверка изменения сообщения (после 2 суток простоя)
@dp.message(Command("test2"))
async def cmd_edit_msg1(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        async with CacheClient() as cache_client:
             cached_messages = await cache_client.get_cache_by_telegram_id(user_id)

        try:
            await bot.edit_message_media(chat_id=message.chat.id,
                                         message_id=cached_messages.get("test_message_id"),
                                         media=InputMediaPhoto(media=Pictures.USER_PROFILE_PICTURE.value,
                                                               caption=f"Сообщение было изменено {datetime.now()}"))
        except TelegramBadRequest as e:
            print(f"ошибка удаления сообщений: {e}")


# проверка username
@dp.message(Command("test4"))
async def cmd_check_username(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        result = await check_username_relevance(bot, ADMIN_ID)
        print("Актуален?" , result)

    await message.delete()


# проверка username
@dp.message(Command("test5"))
async def cmd_check_id(message: types.Message):
    user_id = message.from_user.id
    target_user_id = ASTANA_ID
    if user_id in ADMINS:
        await message.answer("Проверка", reply_markup= await test_button(target_user_id))

    await message.delete()


# проверка изображений
@dp.message(Command("test6"))
async def cmd_check_image(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        for picture in Pictures:
            print(picture.name, picture.value)
            try:
                await message.answer_photo(photo=picture.value)
            except Exception as e:
                print(f"Ошбика с фото {picture.name} - {e}")


# установка описания
@dp.message(Command("set_description"))
async def cmd_set_description(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        # установка описания для бота на разных языках
        for lang, text in DESCRIPTIONS.items():
            try:
                await bot.set_my_description(description=text, language_code=lang)
            except Exception as e:
                print(f"Ошбика установки описания для языка {lang} - {e}")
            else:
                print("Описание для бота установлено ✅")

        # установка короткого описания для бота на разных языках
        for lang, text in SHORT_DESCRIPTIONS.items():
            try:
                await bot.set_my_short_description(short_description=text, language_code=lang)
            except Exception as e:
                print(f"Ошбика установки короткого описания для языка {lang} - {e}")
            else:
                print("Короткое описание для бота установлено ✅")

        # установка имени бота на разных языках
        for lang, name in NAMES.items():
            try:
                await bot.set_my_name(name=name, language_code=lang)
            except Exception as e:
                print(f"Ошбика установки имени для языка {lang} - {e}")
            else:
                print("Название бота установлено ✅")


# ------------------------------------------------------------------ ПОИСК ----------------------------------------------------------


# колбек поиск вход
@dp.callback_query(F.data == "search_menu_start_btn")
async def btn_start_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    username = callback.from_user.username

    # поиск первого подходящего собеседника, получение текста на языке пользователя
    texts = await get_texts(user_lang)

    if not username or username == '':
        await update_user_fields(user_id, username=None)

        picture = Pictures.NO_USERNAME_PICTURE.value
        caption = texts['TEXT']["user_profile"]["username_error"]
        markup = await reload_search_button(texts)
        notification = texts['TEXT']["notifications"]["not_username"]
    
    else:
        target_user, _ = await asyncio.gather(
            find_first_matching_user(user_id),
            update_user_fields(user_id, username=username)
        )

        if target_user:
            picture = target_user.photo_id
            caption, markup = await asyncio.gather(
                get_caption(target_user),
                get_btn_to_search(target_user.first_name, target_user.telegram_id, texts)
                )
            notification = ''

        else:
            picture = Pictures.SEARCH_NOT_FOUND_PICTURE.value
            caption = texts['TEXT']["search_menu"]["not_found"]
            markup = await reload_search_button(texts)
            notification = texts['TEXT']["notifications"]["not_found"]

    # изменение сообщения с текстом "не найдено" и отправка уведомления
    await callback.message.edit_media(media=types.InputMediaPhoto(media=picture, caption=caption),
                                      reply_markup = markup)
    
    await callback.answer(notification)


# обработка колбека реакции
@dp.callback_query(lambda c: c.data.startswith("reaction"))
async def handle_reaction(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    username = callback.from_user.username
    
    _, reaction, target_name, target_tg_id = callback.data.split("|", 3)

    # получение текста на языке пользователя, добавление реакции в базу
    texts, _ = await asyncio.gather(
        get_texts(user_lang),
        add_reaction(user_id, int(target_tg_id), reaction),
    )
    
    await callback.answer(texts["TEXT"]["notifications"][reaction].format(name=target_name)) # уведомление сверху

    if not username or username == '':
        await update_user_fields(user_id, username=None)
        picture = Pictures.NO_USERNAME_PICTURE.value
        caption = texts['TEXT']["user_profile"]["username_error"]
        markup = await reload_search_button(texts)
    
    else:

        # получение первого подходящего собеседника, 
        target_user, _ = await asyncio.gather(
            find_first_matching_user(user_id),
            update_user_fields(user_id, username=username)
        )

        if target_user:
            picture = target_user.photo_id
            caption, markup = await asyncio.gather(
                get_caption(target_user),
                get_btn_to_search(target_user.first_name, target_user.telegram_id, texts)
            )

        else:
            picture = Pictures.SEARCH_NOT_FOUND_PICTURE.value
            caption = texts['TEXT']["search_menu"]["not_found"]
            markup = await reload_search_button(texts)

    await callback.message.edit_media(media=types.InputMediaPhoto(media=picture, caption=caption),
                                      reply_markup = markup)


# колбек повторить поиск
@dp.callback_query(lambda c: c.data.startswith("reload_search"))
async def btn_reload_search(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    username = callback.from_user.username

    texts = await get_texts(user_lang)

    if not username or username == '':
        await update_user_fields(user_id, username=None)
        picture = Pictures.NO_USERNAME_PICTURE.value
        caption = texts['TEXT']["user_profile"]["username_error"]
        markup = await reload_search_button(texts)

    else:
        target_user, _ = await asyncio.gather(
            find_first_matching_user(user_id),
            update_user_fields(user_id, username=username)
            )

        if target_user:
            picture = target_user.photo_id
            caption, markup = await asyncio.gather(
                get_caption(target_user),
                get_btn_to_search(target_user.first_name, target_user.telegram_id, texts)
            )

        else:
            picture = Pictures.SEARCH_NOT_FOUND_PICTURE.value
            caption = texts['TEXT']["search_menu"]["not_found"]
            markup = await reload_search_button(texts)
            await callback.answer(texts['TEXT']["notifications"]["not_found"]) # уведомление сверху

    await callback.message.edit_media(media=types.InputMediaPhoto(media=picture, caption=caption),
                                      reply_markup = markup)


# ------------------------------------------------------------------ СОВПАДЕНИЯ ----------------------------------------------------------


# колбек кнопка старт у меню совпадений
@dp.callback_query(lambda c: c.data.startswith("match_menu_start_btn"))
async def query_start__reload_btn_match_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    username = callback.from_user.username

    texts = await get_texts(user_lang)

    if not username or username == '':
        await update_user_fields(user_id, username=None)
        picture = Pictures.NO_USERNAME_PICTURE.value
        caption = texts['TEXT']["user_profile"]["username_error"]
        markup = await get_empty_menu_buttons(texts)
        notification = texts['TEXT']["notifications"]["not_username"]

    else:
        # получение языка пользователя, кол-во реакции по категориям
        results = await asyncio.gather(
            get_match_targets(user_id),
            get_collection_targets(user_id),
            get_intent_targets(user_id, "LOVE"),
            get_intent_targets(user_id, "SEX"),
            get_intent_targets(user_id, "CHAT"),
            update_user_fields(user_id, username=username)
        )

        # Распаковка результатов
        (_, match_count), (_, collection_count), (_, love_count), (_, sex_count), (_, chat_count), _ = results

        picture = Pictures.MATCH_MENU_PICTURE.value
        caption = ""
        markup = await get_matches_menu_buttons(match_count, collection_count, love_count, sex_count, chat_count, texts)
        notification = texts['TEXT']["notifications"]["reloaded"]

    # изменение сообщения и отправка уведомления
    await callback.message.edit_media(media=InputMediaPhoto(media=picture, caption=caption),
                                      reply_markup = markup)
    await callback.answer(notification)


# колбек кнопка мэтчи в меню Совпадений
@dp.callback_query(F.data == "matches")
async def query_matches(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code

    # получение списка совпедений и текста на языке пользователя
    (target_users_ids, _), texts = await asyncio.gather(
        get_match_targets(user_id),
        get_texts(user_lang)
    )

    if not target_users_ids:
        photo_id = Pictures.MATCH_NOT_FOUND_PICTURE.value
        caption = texts['TEXT']['match_menu']['match_empty']
        markup = await empty_category_buttons(texts)
    else:
        first_id, reaction = next(iter(target_users_ids.items())) #получение первого пользователя и его реакции

        # получение инфо о пользователе и id предыдущего и следующего пользователя в списке
        target_user, (prev_id, next_id) = await asyncio.gather(
            get_user_by_id(first_id),
            get_prev_next_ids(first_id, list(target_users_ids.keys()))
        )

        photo_id = target_user.photo_id

        caption, markup = await asyncio.gather(
            get_caption(target_user, user_lang, reaction),
            get_match_user(target_user, [prev_id, next_id], texts)
        )

    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption),
                                      reply_markup = markup)


# вперед/назад при навигации у меню Совпадений
@dp.callback_query(lambda c: c.data.startswith("navigation_matches"))
async def query_matches_navigation(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    _, target_id = callback.data.split("|", 1)

    if target_id == 'None':
        await callback.answer(texts['TEXT']["notifications"]["empty"]) # уведомление сверху
        return

    target_id = int(target_id)
    target_users_ids, _ = await get_match_targets(user_id)

    target_user, (prev_id, next_id) = await asyncio.gather(
        get_user_by_id(target_id),
        get_prev_next_ids(target_id, list(target_users_ids.keys()))
    )

    reaction = target_users_ids[target_id]
    photo_id = target_user.photo_id

    caption, markup = await asyncio.gather(
        get_caption(target_user, user_lang, reaction),
        get_match_user(target_user, [prev_id, next_id], texts)
    )

    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption),
                                      reply_markup = markup)


# удаление пользователей из match и intentions
@dp.callback_query(lambda c: c.data.startswith("skip_user"))
async def query_skip_user(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    _, reaction, target_id, chosen_id = callback.data.split("|", 3)

    target_id = int(target_id)
    await add_reaction(user_id, target_id, ReactionType.SKIP.value)
    await callback.answer(texts['TEXT']["notifications"]["delete"]) # уведомление сверху

    if reaction == "MATCH":

        if chosen_id == "None":
            photo_id = Pictures.MATCH_NOT_FOUND_PICTURE.value
            caption = texts['TEXT']['match_menu']['match_empty']
            markup = await empty_category_buttons(texts)
        else:
            chosen_id = int(chosen_id)
            target_users_ids, _ = await get_match_targets(user_id)

            target_user, (prev_id, next_id) = await asyncio.gather(
                get_user_by_id(chosen_id),
                get_prev_next_ids(chosen_id, list(target_users_ids.keys()))
            )

            reaction = target_users_ids[chosen_id]
            photo_id = target_user.photo_id

            caption, markup = await asyncio.gather(
                get_caption(target_user, user_lang, reaction),
                get_match_user(target_user, [prev_id, next_id], texts)
            )

        await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption),
                                        reply_markup = markup)
    else:

        if chosen_id == "None":
            photo_id = Pictures.get_not_found_picture(reaction)
            caption = texts['TEXT']['match_menu']['empty'][reaction]
            markup = await empty_category_buttons(texts)
        else:
            chosen_id = int(chosen_id)
            target_users_ids, _ = await get_intent_targets(user_id, reaction)
            target_user, (prev_id, next_id) = await asyncio.gather(
                get_user_by_id(chosen_id),
                get_prev_next_ids(chosen_id, target_users_ids)
            )
            photo_id = target_user.photo_id
            amount = (PRICES.get(user_lang) or PRICES["en"]).get("add_to_collection")
            caption, markup = await asyncio.gather(
                get_caption(target_user),
                get_intention_user(target_user, [prev_id, next_id], reaction, amount, texts)
            )

        await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption),
                                        reply_markup = markup)


# кнопка без действия
@dp.callback_query(F.data == "pass")
async def query_pass(callback: types.CallbackQuery):
    await callback.answer()
    return


# ------------------------------------------------------------------ КОЛЛЕКЦИЯ ----------------------------------------------------------


# колбек кнопка Коллекция в меню Совпадений
@dp.callback_query(F.data == "collection")
async def query_collection(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code

    texts, (target_users_ids, _) = await asyncio.gather(
        get_texts(user_lang),
        get_collection_targets(user_id)
    )

    if not target_users_ids:
        photo_id = Pictures.COLLECTION_NOT_FOUND_PICTURE.value
        caption = texts['TEXT']['match_menu']['collection_empty']
        markup = await empty_category_buttons(texts)

    else:
        target_user, (prev_id, next_id) = await asyncio.gather(
            get_user_by_id(target_users_ids[0]),
            get_prev_next_ids(target_users_ids[0], target_users_ids)
        )

        photo_id = target_user.photo_id

        caption, markup = await asyncio.gather(
            get_caption(target_user),
            get_collection_user(target_user, [prev_id, next_id], texts)
        )

    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption),
                                      reply_markup = markup)
    

# вперед/назад при навигации Коллекция
@dp.callback_query(lambda c: c.data.startswith("navigation_collection"))
async def query_collection_navigation(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code

    texts = await get_texts(user_lang)

    _, target_id = callback.data.split("|", 1)

    if target_id == 'None':
        await callback.answer(texts['TEXT']["notifications"]["empty"]) # уведомление сверху
        return

    target_id = int(target_id)
    target_users_ids, _ = await get_collection_targets(user_id)

    target_user, (prev_id, next_id) = await asyncio.gather(
        get_user_by_id(target_id),
        get_prev_next_ids(target_id, target_users_ids)
    )

    caption, markup = await asyncio.gather(
        get_caption(target_user),
        get_collection_user(target_user, [prev_id, next_id], texts)
    )

    await callback.message.edit_media(media=InputMediaPhoto(media=target_user.photo_id, caption=caption),
                                      reply_markup = markup)


# ------------------------------------------------------------------ НАМЕРЕНИЯ ----------------------------------------------------------


# колбека кому нравишься
@dp.callback_query(lambda c: c.data.startswith("intentions"))
async def handle_who_wants(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    
    _, reaction = callback.data.split("|", 1)

    (target_users_ids, _), texts = await asyncio.gather(
        get_intent_targets(user_id, reaction), 
        get_texts(user_lang)
    )

    if not target_users_ids:
        photo_id = Pictures.get_not_found_picture(reaction)
        caption = texts['TEXT']['match_menu']['empty'][reaction]
        markup = await empty_category_buttons(texts)
    else:
        target_user, (prev_id, next_id) = await asyncio.gather(
            get_user_by_id(target_users_ids[0]),
            get_prev_next_ids(target_users_ids[0], target_users_ids)
        )
        photo_id = target_user.photo_id
        amount = (PRICES.get(user_lang) or PRICES["en"]).get("add_to_collection")
        caption, markup = await asyncio.gather(
            get_caption(target_user),
            get_intention_user(target_user, [prev_id, next_id], reaction, amount, texts)
        )

    await callback.message.edit_media(media=InputMediaPhoto(media=photo_id, caption=caption),
                                      reply_markup = markup)


# вперед/назад при навигации Коллекция
@dp.callback_query(lambda c: c.data.startswith("navigation_intentions"))
async def query_wants_navigation(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    texts = await get_texts(user_lang)

    _, reaction, target_id = callback.data.split("|", 2)

    if target_id == 'None':
        await callback.answer(texts['TEXT']["notifications"]["empty"]) # уведомление сверху
        return

    target_id = int(target_id)
    target_users_ids, _ = await get_intent_targets(user_id, reaction)

    target_user, (prev_id, next_id) = await asyncio.gather(
        get_user_by_id(target_id),
        get_prev_next_ids(target_id, target_users_ids)
    )

    amount = (PRICES.get(user_lang) or PRICES["en"]).get("add_to_collection")
    caption, markup = await asyncio.gather(
        get_caption(target_user),
        get_intention_user(target_user, [prev_id, next_id], reaction, amount, texts)
    )

    await callback.message.edit_media(media=InputMediaPhoto(media=target_user.photo_id, caption=caption),
                                      reply_markup = markup)


# обработка колбека оплаты
@dp.callback_query(lambda c: c.data.startswith("pay_intentions"))
async def handle_intentions_pay(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_lang = callback.from_user.language_code
    
    _, target_id, amount_str, reaction = callback.data.split("|")
    target_id = int(target_id)
    amount = int(amount_str)

    target_user, texts = await asyncio.gather(
        get_user_by_id(target_id),
        get_texts(user_lang)
    )
    try:
        target_username = await check_username_relevance(bot, target_user.telegram_id)
    except Exception as e:
        print(f"Ошибка получения username: {e}")
        target_username = target_user.username

    if target_username:
        label = texts["TEXT"]["payment"]["collection"]["label"].format(target_name=target_user.first_name)
        title = texts["TEXT"]["payment"]["collection"]["title"].format(target_name=target_user.first_name)
        description = texts["TEXT"]["payment"]["collection"]["description"].format(target_name=target_user.first_name)

        prices = [LabeledPrice(label=label, amount=amount)] #🏆 💫 ⭐ Избранное

        cached_messages, _ = await asyncio.gather(
            get_cached_messages_ids(user_id),
            update_user_fields(target_user.telegram_id, username = target_username)
        )

        pay_message_id = cached_messages.get('collection_pay_message_id')
        if pay_message_id:
            try:
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=pay_message_id)
            except TelegramBadRequest as e:
                print(f"ошибка удаления сообщений: {e}")

        sent_invoice = await callback.message.answer_invoice(
            title=title,
            description=description,
            payload=f"payment_add_to_collection|{target_id}|{amount}|{reaction}",
            provider_token="",
            currency="XTR",
            prices=prices,
            reply_markup=payment_keyboard(texts)
        )

        # сохраняем в Кэш
        await save_to_cache(callback.from_user.id, "collection_pay_message_id", message_id = sent_invoice.message_id)
        await callback.answer(texts["TEXT"]["notifications"]["payment_sent"])

    else:
        # получение списка пользователей по реакции, обновление инфо о пользователе
        (target_users_ids, _), _ = await asyncio.gather(
            get_intent_targets(user_id, reaction),
            update_user_fields(target_user.telegram_id, username = None)
        )
        
        if not target_users_ids:
            photo_id = Pictures.get_not_found_picture(reaction)
            caption = texts['TEXT']['match_menu']['empty'][reaction]
            markup = await empty_category_buttons(texts)
        else:
            target_user, (prev_id, next_id) = await asyncio.gather(
                get_user_by_id(target_users_ids[0]),
                get_prev_next_ids(target_users_ids[0], target_users_ids)
            )

            photo_id = target_user.photo_id

            amount = (PRICES.get(user_lang) or PRICES["en"]).get("add_to_collection")
            caption, markup = await asyncio.gather(
                get_caption(target_user),
                get_intention_user(target_user, [prev_id, next_id], reaction, amount, texts)
            )
        
        await callback.message.edit_media(media=types.InputMediaPhoto(media=photo_id, caption=caption),
                                          reply_markup = markup)
        
        await callback.answer(texts["TEXT"]["notifications"]["unavailable"].format(name=target_user.first_name))


# ------------------------------------------------------------------- ОПЛАТА -------------------------------------------------------


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(lambda message: message.successful_payment is not None)
async def on_successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    # получение текста на языке пользователя
    texts = await get_texts(user_lang)

    # получение id сообщений
    async with CacheClient() as cache_client:
        cached_messages = await cache_client.get_cache_by_telegram_id(user_id)

    # добавление в коллекцию
    if payload.startswith("payment_add_to_collection"):
        _, target_id, amount, reaction = payload.split("|")

        async with PaymentClient() as payment_client:
            new_payment = Payment(telegram_id=user_id, amount=int(amount), payment_type=PaymentType.COLLECTION.value, target_tg_id=int(target_id))
            await payment_client.insert_payment(new_payment)

        async with CacheClient() as cache_client:
            cached_messages = await cache_client.get_cache_by_telegram_id(user_id)

        payment_message_id = cached_messages.get("collection_pay_message_id")

        # получение списка пользователей из коллекции, получение id сообщений, добавление платежа в бд
        # ///////////////////////////// 000000000
        target_users_ids, _,  = await get_intent_targets(user_id, reaction)
        
        async with CacheClient() as cache_client:
            await cache_client.delete_cache_by_telegram_id_and_parameter(user_id, "collection_pay_message_id")

        if not target_users_ids:
            photo_id = Pictures.get_not_found_picture(reaction)
            caption = texts['TEXT']['match_menu']['empty'][reaction]
            markup = await empty_category_buttons(texts)
        else:
            async with UserClient() as user_client:
                target_user, (prev_id, next_id) = await asyncio.gather(
                    user_client.get_user_by_id(target_users_ids[0]),
                    get_prev_next_ids(target_users_ids[0], target_users_ids)
                )

            photo_id = target_user.photo_id

            amount = (PRICES.get(user_lang) or PRICES["en"]).get("add_to_collection")
            caption, markup = await asyncio.gather(
                get_caption(target_user),
                get_intention_user(target_user, [prev_id, next_id], reaction, amount, texts)
            ) #/////////////////////////////////////////

        await bot.edit_message_media(chat_id=message.chat.id,
                                     message_id=cached_messages.get("match_menu_message_id"),
                                     media=InputMediaPhoto(media=photo_id, caption=caption),
                                     reply_markup = markup)

    # активация инкогнито
    elif payload.startswith("payment_incognito"):
        _, amount = payload.split("|")
        
        # добавление инфо о платеже в базу, обновление статусов у пользователя, удаление кэша
        async with PaymentClient() as payment_client, UserClient() as user_client, CacheClient() as cache_client:
            new_payment = Payment(user_id, int(amount), PaymentType.INCOGNITO)
            await asyncio.gather(
                payment_client.insert_payment(new_payment),
                user_client.update_user_fields(user_id, incognito_pay=True, incognito_switch=True),
                cache_client.delete_cache_by_telegram_id_and_parameter(user_id, "incognito_pay_message_id")
            )

        # изменение стартового сообщения
        await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                            message_id=cached_messages.get("start_message_id"),
                                            reply_markup=await get_profile_edit_buttons(True, True, texts))

        # получаем id из Кэш и удаляем сообщение
        async with CacheClient() as cache_client:
            cached_messages = await cache_client.get_cache_by_telegram_id(user_id)

        payment_message_id = cached_messages.get("incognito_pay_message_id")

    await bot.delete_message(chat_id=message.chat.id, message_id=payment_message_id)


# ------------------------------------------------------------------- ТЕКСТ (Последний шаг в Анкете)-------------------------------------------------------


# обработка текста - добавляет или изменяет описание "о себе"
@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    # получение инфо о пользователе
    async with UserClient() as user_client:
        user = await user_client.get_user_by_id(user_id)

    # защита от повторов, удаление текста
    if user.about_me or not user.photo_id:
        await message.delete()
        return
    
    # получение id стартового сообщения, текста на языке пользователя
    async with CacheClient() as cache_client:
        cached_messages, texts = await asyncio.gather(
            cache_client.get_cache_by_telegram_id(user_id),
            get_texts(user_lang)
        )

    start_message_id = cached_messages.get("start_message_id")
    match_menu_message_id = cached_messages.get("match_menu_message_id")
    search_menu_message_id = cached_messages.get("search_menu_message_id")

    user_text = message.text
    if len(user_text) >= MIN_COUNT_SYMBOLS and len(user_text) <= MAX_COUNT_SYMBOLS:
        # обновить инфо о пользователе в базе, изменить стартовое сообщение
        async with UserClient() as user_client:
            await user_client.update_user_fields(user_id, about_me = user_text)
        
        await bot.edit_message_media(chat_id=message.chat.id,
                                     message_id=start_message_id,
                                     media=InputMediaPhoto(media=user.photo_id,
                                                           caption=texts['TEXT']["user_profile"]["profile"].format(first_name=user.first_name,
                                                                                                                 country_local=user.country_local,
                                                                                                                 city_local=user.city_local,
                                                                                                                 gender=texts['GENDER_LABELS'][user.gender],
                                                                                                                 gender_emoji=texts['GENDER_EMOJI'][user.gender],
                                                                                                                 gender_search=texts['GENDER_SEARCH_LABELS'][user.gender_search],
                                                                                                                 about_me=user_text)),
                                    reply_markup = await get_profile_edit_buttons(user.incognito_pay, user.incognito_switch, texts))
        
        d = [{'parameter': 'match_menu_message_id',
              'message_id': match_menu_message_id,
              'photo_id': Pictures.MATCH_MENU_PICTURE.value,
              'caption': texts['TEXT']['match_menu']['start'],
              'markup': await get_start_button_match_menu(texts)},

              {'parameter': 'search_menu_message_id',
               'message_id': search_menu_message_id,
               'photo_id': Pictures.SEARCH_MENU_PICTURE.value,
               'caption': texts['TEXT']['search_menu']['start'],
               'markup': await get_start_button_search_menu(texts)}
              ]
        
        for el in d:
            parameter = el.get('parameter')
            message_id = el.get('message_id')
            caption = el.get('caption')
            photo_id = el.get('photo_id')
            markup = el.get('markup')

            if message_id:
                await bot.edit_message_media(chat_id=message.chat.id,
                                             message_id=message_id,
                                             media=InputMediaPhoto(media=photo_id, caption=caption),
                                             reply_markup = markup)
            else:
                msg = await message.answer_photo(photo=photo_id, caption=caption, reply_markup=markup)
                async with CacheClient() as cache_client:
                    new_cache = Cache(user_id, parameter, message_id = msg.message_id)
                    await cache_client.insert_cache(new_cache)

    else:
        if len(user_text) < MIN_COUNT_SYMBOLS:
            caption=texts['TEXT']['user_profile']['min_count_symbols_error'].format(MIN_COUNT_SYMBOLS=MIN_COUNT_SYMBOLS, text_length=len(user_text)),

        if len(user_text) > MAX_COUNT_SYMBOLS:
            caption=texts['TEXT']['user_profile']['max_count_symbols_error'].format(MAX_COUNT_SYMBOLS=MAX_COUNT_SYMBOLS, text_length=len(user_text))

        await bot.edit_message_caption(chat_id=message.chat.id, message_id=start_message_id, caption=caption, reply_markup = None)
    
    await message.delete() # удаляем сообщение пользователя


# ------------------------------------------------------------------- Обработка других форматов -------------------------------------------------------


@dp.message(~(F.text | F.photo | F.location))
async def delete_unwanted(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"⚠️ Не удалось удалить сообщение: {e}")
