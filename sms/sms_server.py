import logging.config

import responder

from sms.subroute.auth import auth_api
from sms.subroute.sms import sms_api

logging.config.fileConfig("log.ini")

logger = logging.getLogger(__name__)

api = responder.API(
    title="SMS Web Service",
    version="1.0",
    openapi="3.0.0",
    docs_route="/docs",
    static_dir="static",
)


@api.route("/test")
async def welcome(req, resp):
    from sms.util.db import _db

    resp.media = {
        "Welcome": "Welcome To SMS Web Services!",
        "db": str(_db and _db.db),
    }


api.add_route("/", static=True)

api.mount("/auth", auth_api)
api.mount("/sms", sms_api)

if __name__ == "__main__":
    api.run(address="0.0.0.0", port=5000)
