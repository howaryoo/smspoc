# -*- coding: utf-8 -*-
class SMSException(Exception):
    pass


class BadToken(SMSException):
    pass


class BadVerificationCode(SMSException):
    pass


class NoCredit(SMSException):
    pass


class NotVerified(SMSException):
    pass
