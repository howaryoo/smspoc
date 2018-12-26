# -*- coding: utf-8 -*-
from dataclasses import dataclass

from sms.model.base import Base


@dataclass
class User(Base):
    login: str
    password: str
    mobile: str
    confirmation: str
    sms_verified: bool = False
    balance: int = 0
