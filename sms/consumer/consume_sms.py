# -*- coding: utf-8 -*-
import asyncio
import logging.config

import nexmo
from aio_pika import connect_robust, IncomingMessage

from sms.configuration.environment import (
    RABBITMQ_HOST,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    ROUTING_KEY, UNIT_COST, NEXMO_KEY, NEXMO_SECRET)
from sms.model.message import Message
from sms.service import sms
from sms.util.json import loads

logger = logging.getLogger("sms")

sms_client = nexmo.Client(key=NEXMO_KEY, secret=NEXMO_SECRET)


async def on_message(message: IncomingMessage):
    body = loads(message.body)
    message = Message(msg_from=body["From"], msg_to=body["to"],
                      message=body["message"], balance=0)

    user = await sms.check_balance(message.msg_from)
    balance = user.balance - UNIT_COST
    user.balance = balance
    message.balance = balance
    user.save(_key_field="login")
    message.save()

    sms_client.send_message({
        'from': message.msg_from,
        'to': message.msg_to,
        'text': message.message,
    })
    logger.info("Message for user: %s sent. Balance: %s", user.login, balance)


async def main(loop):
    connection = await connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/", loop=loop)

    channel = await connection.channel()

    queue = await channel.declare_queue(ROUTING_KEY)

    await queue.consume(on_message, no_ack=True)


if __name__ == "__main__":
    logging.config.fileConfig("log.ini")

    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    logger.info("SMS consumer starting")

    loop.run_forever()
