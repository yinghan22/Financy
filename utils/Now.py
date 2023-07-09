import uuid
from datetime import datetime


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _uuid():
    return uuid.uuid1().hex
