import json
from ydb_logic import dp, bot, logger


async def handler(event, context):
    """
    Entry point (index.handler)
    """
    messages = event.get("messages", [])

    # Логируем количество и тип сообщений
    logger.info(f"Всего сообщений: {len(messages)}")

    for msg in messages:
        details = msg.get("details", {})
        message = details.get("message", {})
        body_str = message.get("body")

        # Логируем само тело (даже если это ping)
        logger.info(f"BODY: {body_str}")

        if not body_str:
            continue

        try:
            body = json.loads(body_str)
        except Exception as e:
            logger.error(f"Ошибка парсинга body: {e}")
            continue

        # Если это ping — просто логируем
        if body.get("ping"):
            logger.info("⚙️ Получен ping — бот пробуждён")
            continue

        # Иначе — Telegram update
        await dp.feed_webhook_update(bot=bot, update=body)

    return {'statusCode': 200}

