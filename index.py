import json
from main import dp, bot


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