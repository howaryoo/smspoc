# -*- coding: utf-8 -*-
import logging
import secrets
from datetime import datetime

import nexmo

from sms.configuration.environment import UNIT_COST, OFFERED_UNITS, NEXMO_KEY, NEXMO_SECRET
from sms.model.token import Token
from sms.model.user import User
from sms.util.db import async_execute
from sms.util.exceptions import BadVerificationCode

logger = logging.getLogger(__name__)

sms_client = nexmo.Client(key=NEXMO_KEY, secret=NEXMO_SECRET)


async def get_user(user_name):
    aql_query = """
        FOR u in User
        FILTER u.login == @login
        LIMIT 1
        RETURN u"""
    bind_vars = {"login": user_name}
    async for user in async_execute(aql_query, bind_vars):
        return user


async def register(login, password, mobile):
    confirmation = secrets.token_urlsafe(3)
    user = User(login, password, mobile, confirmation)
    # FIXME: encrypt password
    user.save(_key_field="login")
    # send confirmation SMS
    # Fixme make non blocking
    sms_client.send_message({
        'from': 'SMS service',
        'to': mobile,
        'text': f'Your code is: {confirmation}',
    })

    return user


async def login(user_name, password):
    user_d = await get_user(user_name)
    if user_d["password"] == password:
        token = secrets.token_urlsafe(8)
        created = datetime.now()
        new_token = Token(login=user_name, token=token, created=created)
        new_token.save(_key_field="login")
        return new_token.token


async def get_token(token):
    aql_query = """
        FOR t in Token
        FILTER t.token == @token
        LIMIT 1
        RETURN t.login"""
    bind_vars = {"token": token}
    async for username in async_execute(aql_query, bind_vars):
        return username


async def check_token(token):
    return await get_token(token)


async def verify(user, confirmation):
    user_d = await get_user(user)
    if user_d["confirmation"] == confirmation:
        user = User(user_d["login"], user_d["password"],
                    user_d["mobile"], user_d["confirmation"], sms_verified=True,
                    balance=UNIT_COST * OFFERED_UNITS)
        user.save(_key_field="login")
        return True
    else:
        raise BadVerificationCode(f"Bad verification code for user: {user}")
