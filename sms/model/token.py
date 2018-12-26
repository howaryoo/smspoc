# -*- coding: utf-8 -*-
from datetime import datetime
from dataclasses import dataclass

from sms.model.base import Base


@dataclass
class Token(Base):
    login: str
    token: str
    created: datetime
    updated: datetime = None
