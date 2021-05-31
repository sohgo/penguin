from datetime import datetime, timedelta
from hashlib import sha256
from random import random

"""
xpath and token map.
    - generate token.
    - validate token.
    - house keeping the map.
"""
class XTokenMap():

    def __init__(self, lifetime=7200, limit=1000, hard_limit=1300):
        """
        check if the length of xtmap is less than the hard_limit.
        if it exceeds, remove items matched with the following criteria.
        1. remove items exceed the lifetime in seconds.
        2. remove items until the length of xtmap become less than the limit.
        """
        self.xtmap = {}
        self.lifetime = lifetime
        self.limit = limit
        self.hard_limit = hard_limit

    def _gen_token(self):
        m = sha256()
        m.update((str(random())+str(datetime.now().timestamp())).encode())
        return m.hexdigest()

    def _housekeeping(self):
        # check hard limit.
        if len(self.xtmap) < self.hard_limit:
            return
        # remove expired items.
        for kv in list(self.xtmap.items()):
            # delete map if it is older than a certain time.
            now = datetime.now()
            if now - timedelta(seconds=self.lifetime) > kv[1]["accessed"]:
                self.xtmap.pop(kv[0])
        # remove oldest items.
        if len(self.xtmap) >= self.limit:
            # don't need sorting because of python dict order.
            self.xtmap = dict(list(self.xtmap.items())[:self.limit])

    def generate_token(self, xpath=None):
        self._housekeeping()
        token = self._gen_token()
        now = datetime.now()
        self.xtmap.update({token: {"xpath": xpath, "accessed": now}})
        return token

    def validate_token(self, token, xpath=None):
        self._housekeeping()
        v = self.xtmap.get(token)
        if v is not None:
            if xpath is not None:
                if xpath == v["xpath"]:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def remove_token(self, token):
        for k in list(self.xtmap.keys()):
            if k == token:
                del(k)
                break
        else:
            raise ValueError

    def counts(self):
        return len(self.xtmap)

if __name__ == "__main__":
    import time
    xtmap = XTokenMap()
    t1 = xtmap.generate_token()
    print(xtmap.validate_token(t1))
    print(xtmap.validate_token("5ecd5c301ac34bca3a57709edf3e1e9e07f9fcc07369bd989141951e12df8e45"))
    #
    xtmap = XTokenMap(limit=5, hard_limit=10)
    for i in range(15):
        xtmap.generate_token()
        print("len=", xtmap.counts())
    #
    xtmap = XTokenMap(lifetime=5, limit=5, hard_limit=7)
    for i in range(10):
        xtmap.generate_token()
        print("len=", xtmap.counts())
        time.sleep(1)
