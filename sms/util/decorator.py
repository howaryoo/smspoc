# -*- coding: utf-8 -*-
from functools import wraps

from sms.service import auth


def http_error(logger):
    """
    A decorator for responder's route functions that
     * logs exception
     * set a 400 status code
    @param logger:
    """
    def decorate(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            _, req, resp = args[:3]
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                resp.status_code = 400
                resp.media = {"error": str(exc)}
                logger.exception("%s on %s failed", req.method, req.full_url)

        return wrapper
    return decorate


def require_auth(func):
    """
    A decorator for responder's route functions that
     * checks the auth token, provides user as first argument
     * sets a 401 status code if bad token
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        _, req, resp = args[:3]
        token = req.headers["sms-token"]
        user = await auth.check_token(token)
        if user:
            kwargs["user"] = user
            return await func(*args, **kwargs)
        else:
            resp.status_code = 401
            resp.media = {"error": "Unauthorized"}

    return wrapper
