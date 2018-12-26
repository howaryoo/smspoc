import logging

import responder

from sms.service import auth
from sms.util.decorator import require_auth, http_error

logger = logging.getLogger(__name__)

auth_api = responder.API(static_dir="static")


@auth_api.route("/auth/register")
class Register:
    async def on_post(self, req, resp):
        credentials = await req.media()
        login = credentials["login"]
        password = credentials["password"]
        mobile = credentials["mobile"]

        user = await auth.register(login, password, mobile)
        resp.media = {"message": f"registered user {user.login}"}


@auth_api.route("/auth/login")
class Login:
    async def on_post(self, req, resp):
        credentials = await req.media()
        login = credentials["login"]
        password = credentials["password"]
        token = await auth.login(login, password)

        resp.media = {"sms-token": token}


@auth_api.route("/auth/verify")
class Verify:
    @http_error(logger)
    @require_auth
    async def on_post(self, req, resp, *, user):
        credentials = await req.media()
        confirmation = credentials["confirmation"]
        is_confirmed = await auth.verify(user, confirmation)
        resp.media = {"verified": is_confirmed}

