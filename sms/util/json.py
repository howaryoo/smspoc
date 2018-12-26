# -*- coding: utf-8 -*-
import dataclasses
import datetime
import json


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super().default(obj)


def dumps(din):
    return json.dumps(din, cls=DataclassJSONEncoder)


def loads(sin):
    return json.loads(sin)
