# -*- coding: utf-8 -*-
import logging
from dataclasses import dataclass

from arango.exceptions import DocumentUpdateError, DocumentParseError

from sms.util.db import db
from sms.util.json import loads, dumps

logger = logging.getLogger(__name__)


@dataclass
class Base:

    def dumps(self):
        return dumps(self)

    def save(self, _key_field=None):
        collection_name = self.__class__.__name__
        with db() as db_conn:
            collection = db_conn.db.collection(collection_name)
            data = loads(self.dumps())
            try:
                if _key_field:
                    data["_key"] = data.get(_key_field)
                collection.update(data)
            except (DocumentUpdateError, DocumentParseError):
                collection.insert(data)

    def find(self, key, value):
        collection_name = self.__class__.__name__
        with db() as db_conn:
            collection = db_conn.db.collection(collection_name)
            doc = collection.find({key: value})
            if doc:
                return doc
