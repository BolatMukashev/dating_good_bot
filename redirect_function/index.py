import aiobotocore.session
from config import logger, QUEUE_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


async def send_to_queue(body: str):
    """Публикация апдейта в Yandex Message Queue"""
    session = aiobotocore.session.get_session()
    async with session.create_client(
        "sqs",
        endpoint_url="https://message-queue.api.cloud.yandex.net",
        region_name="ru-central1",
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
    ) as client:
        await client.send_message(QueueUrl=QUEUE_URL, MessageBody=body)


async def handler(event, context):
    messages = event.get("messages", [])
    logger.info(f"Всего сообщений: {len(messages)}")

    for msg in messages:
        details = msg.get("details", {})
        message = details.get("message", {})
        body_str = message.get("body")

        if not body_str:
            continue

        logger.info(f"BODY: {body_str}")

        # просто кладём в очередь
        await send_to_queue(body_str)

    # моментально возвращаем Telegram'у 200 OK
    return {'statusCode': 200}
