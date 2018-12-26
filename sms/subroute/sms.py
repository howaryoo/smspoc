import logging

import responder

from sms.service import sms
from sms.util.decorator import http_error, require_auth

logger = logging.getLogger(__name__)

sms_api = responder.API(static_dir="static")


@sms_api.route("/sms/queue")
class Queue:
    @http_error(logger)
    @require_auth
    async def on_post(self, req, resp, *, user):
        sms_payload = await req.media()
        sms_payload["From"] = user

        await sms.check_balance(user)
        await sms.publish_sms(sms_payload)
        resp.media = {"message": "published"}
