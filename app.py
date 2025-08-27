import os
import asyncio
from aiohttp import web
from db_connect import async_engine
from models import Base
from config import *
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram import Bot
from main import logger, bot, dp


# ------------------------------------------------------------------- Активация бота -------------------------------------------------------
async def on_startup(bot: Bot) -> None:
    """Функция выполняется при старте приложения"""
    try:
        # Создаем таблицы базы данных
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Устанавливаем webhook
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query", "pre_checkout_query"]
        )
        
        logger.info(f"✅ Webhook установлен: {WEBHOOK_URL}")
        
        # Получаем информацию о webhook
        webhook_info = await bot.get_webhook_info()
        logger.info(f"📋 Webhook info: {webhook_info}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при установке webhook: {e}")
        raise


async def on_shutdown(bot: Bot) -> None:
    """Функция выполняется при остановке приложения"""
    try:
        await bot.delete_webhook()
        logger.info("🔥 Webhook удален")
    except Exception as e:
        logger.error(f"❌ Ошибка при удалении webhook: {e}")


def create_app() -> web.Application:
    """Создает и настраивает веб-приложение"""
    
    # Создаем веб-приложение
    app = web.Application()
    
    # Добавляем здоровье проверку
    async def health_check(request):
        return web.Response(text="Bot is running!", status=200)
    
    app.router.add_get("/health", health_check)
    app.router.add_get("/", health_check)
    
    # Настраиваем webhook handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    
    # Регистрируем webhook path
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Настраиваем приложение с диспетчером
    setup_application(app, dp, bot=bot)
    
    # Добавляем startup и shutdown хэндлеры
    app.on_startup.append(lambda app: on_startup(bot))
    app.on_shutdown.append(lambda app: on_shutdown(bot))
    
    return app


# ------------------------------------------------------------------- Локальный запуск (для разработки) -------------------------------------------------------

async def main_polling():
    """Функция для локального запуска с polling (для разработки)"""
    try:
        # Создаем таблицы базы данных
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Удаляем webhook если он был установлен
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🧹 Webhook удален для polling режима")
        
        # Запускаем polling
        logger.info("🚀 Запуск бота в режиме polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка в polling режиме: {e}")
        raise
    finally:
        await bot.session.close()


# ------------------------------------------------------------------- Точка входа -------------------------------------------------------

if __name__ == '__main__':
    # Проверяем переменную окружения для выбора режима
    
    if BOT_MODE == 'polling':
        # Локальная разработка - используем polling
        logger.info("🔧 Режим разработки: Polling")
        asyncio.run(main_polling())
    else:
        # Продакшен - используем webhook
        logger.info("🚀 Продакшен режим: Webhook")
        app = create_app()
        
        # Для локального тестирования webhook
        if LOCAL_WEBHOOK:
            web.run_app(app, host='0.0.0.0', port=PORT)
        else:
            # Для продакшена (например, на Heroku, Railway, etc.)
            port = int(os.getenv('PORT', PORT))
            web.run_app(app, host='0.0.0.0', port=port)

            