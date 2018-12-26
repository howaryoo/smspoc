# -*- coding: utf-8 -*-
import asyncio
import logging
import typing
from contextlib import contextmanager
from dataclasses import dataclass

import requests
from arango import ArangoClient, AQLQueryExecuteError, ServerConnectionError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from sms.configuration.environment import (
    ARANGODB_CORE_HOST,
    ARANGODB_CORE_PORT,
    ARANGODB_DB,
    ARANGODB_USER,
    ARANGODB_PASSWORD,
)

logger = logging.getLogger(__name__)

_db = None


@dataclass
class DB:
    db: "typing.Any"
    async_db: "typing.Any"
    async_aql: "typing.Any"


def connect_db():
    global _db
    client = ArangoClient(
        protocol="http", host=ARANGODB_CORE_HOST, port=ARANGODB_CORE_PORT
    )

    db_client = client.db(
        name=ARANGODB_DB, username=ARANGODB_USER, password=ARANGODB_PASSWORD
    )
    logger.info(
        "Connected to DB: %s/%s %s", ARANGODB_CORE_HOST, ARANGODB_CORE_PORT, ARANGODB_DB
    )

    async_db = db_client.begin_async_execution(return_result=True)
    async_aql = async_db.aql

    _db = DB(db=db_client, async_db=async_db, async_aql=async_aql)
    return _db


@contextmanager
def db():
    global _db
    try:
        if _db:
            yield _db
        else:
            logger.warning(
                "Connecting or RE-connecting to DB: %s/%s %s",
                ARANGODB_CORE_HOST,
                ARANGODB_CORE_PORT,
                ARANGODB_DB,
            )
            _db = connect_db()
            yield _db
    except Exception:
        logger.exception("Could not query DB")
        _db = None
        raise


@retry(retry=retry_if_exception_type(ServerConnectionError), stop=stop_after_attempt(2))
@retry(
    retry=retry_if_exception_type(requests.exceptions.ConnectionError),
    wait=wait_fixed(10),
)
async def async_execute(aql_query, bind_vars=None):
    with db() as db_conn:
        if not bind_vars:
            bind_vars = {}

        # non blocking call (no await needed)
        job = db_conn.async_aql.execute(aql_query, bind_vars=bind_vars)

        while job.status() != "done":
            await asyncio.sleep(0.2)
        try:
            cursor = job.result()
        except AQLQueryExecuteError:
            logger.exception("query: %s failed", aql_query)
            raise
        else:
            has_more = True
            while has_more:
                batch_results = cursor.batch()
                for result in batch_results:
                    yield result
                has_more = cursor.has_more()
