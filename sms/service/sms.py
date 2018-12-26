# -*- coding: utf-8 -*-
import logging

import aio_pika

from sms.configuration.environment import (
    RABBITMQ_HOST,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    UNIT_COST, ROUTING_KEY)
from sms.model.user import User
from sms.service import auth
from sms.util.exceptions import NoCredit, NotVerified
from sms.util.json import dumps

logger = logging.getLogger(__name__)


async def check_balance(user_name):
    user = await auth.get_user(user_name)
    if not user["sms_verified"]:
        raise NotVerified(f"mobile number of user: {user_name} not verified")
    if user["balance"] < UNIT_COST:
        raise NoCredit(f"user: {user_name} has no credit")

    return User(user["login"], user["password"], user["mobile"],
                user["confirmation"], user["sms_verified"], user["balance"])


async def publish_sms(payload):
    # TODO use global connection
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/")

    async with connection:
        routing_key = ROUTING_KEY

        channel = await connection.channel()

        await channel.declare_queue(routing_key)

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=dumps(payload).encode()
            ),
            routing_key=routing_key
        )
