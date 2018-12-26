# -*- coding: utf-8 -*-
import os

ARANGODB_CORE_HOST = os.getenv("ARANGODB_CORE_HOST") or "localhost"
ARANGODB_CORE_PORT = os.getenv("ARANGODB_CORE_PORT") or 8529
ARANGODB_DB = os.getenv("ARANGODB_DB") or "SMS"
ARANGODB_USER = os.getenv("ARANGODB_USER") or "root"
ARANGODB_PASSWORD = os.getenv("ARANGODB_PASSWORD") or "root"

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

ROUTING_KEY = "sms_queue"

NEXMO_KEY = os.getenv("NEXMO_KEY")
NEXMO_SECRET = os.getenv("NEXMO_SECRET")

UNIT_COST = 10
OFFERED_UNITS = 100
