import json
from ydb_logic import dp, bot
from aiogram.exceptions import TelegramNetworkError


async def handler(event, context):
    """
    Entry point
    Точка входа в функцию
    (index.handler)
    """
    #request_body_dict = json.loads(event['body'])
    request_body_dict = json.loads(event["messages"][0]["details"]["message"]["body"])
    await dp.feed_webhook_update(bot=bot, update=request_body_dict)
    return {
        'statusCode': 200
    }


async def ping(event, context):
    """
    Пинг-функция для проверки, жив ли бот.
    Используется облачным триггером (ping).
    """
    try:
        me = await bot.get_me()
        print(f"✅ Bot is alive: {me.username}")
        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True, "username": me.username})
        }
    except TelegramNetworkError:
        print("❌ Network error — бот недоступен")
        return {
            "statusCode": 503,
            "body": json.dumps({"ok": False, "error": "network"})
        }
    except Exception as e:
        print(f"❌ Ping failed: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)})
        }
    

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(ping(None, None))

