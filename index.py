import json
from ydb_logic import dp, bot
from aiogram.exceptions import TelegramNetworkError


async def handler(event, context):
    """
    Entry point
    Точка входа в функцию
    (index.handler)
    """

    # "будильник" для функции
    if isinstance(event, dict) and event.get("ping"):
        print("🌙 Ping received, keeping function warm")
        return {"statusCode": 200, "body": json.dumps({"ok": True})}
    

    #request_body_dict = json.loads(event['body'])
    request_body_dict = json.loads(event["messages"][0]["details"]["message"]["body"])
    await dp.feed_webhook_update(bot=bot, update=request_body_dict)
    return {
        'statusCode': 200
    }


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(ping(None, None))

