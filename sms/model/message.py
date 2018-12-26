# -*- coding: utf-8 -*-
from dataclasses import dataclass

from sms.model.base import Base


@dataclass
class Message(Base):
    msg_from: str
    msg_to: str
    message: str
    balance: int
