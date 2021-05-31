from dateutil import tz
from hashlib import sha256
from datetime import datetime
from random import random

def get_hash():
    m = sha256()
    m.update((str(random())+str(datetime.now().timestamp())).encode())
    return m.hexdigest()

def get_timestamp(TZ="Asia/Tokyo"):
    return datetime.now(tz=tz.gettz(TZ)).isoformat(timespec="seconds")

