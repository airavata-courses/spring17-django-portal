from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings
import redis
import uuid

DJANGO_SESSION='django_sessions'

class RedisIterator:

    def __init__(self,redis_client,name,type="keys"):
        self._redis_client=redis_client
        self._name=name
        self._type=type
        if type == 'keys':
            self._ret_function=self._return_keys
        elif type == 'values':
            self._ret_function=self._return_values
        elif type == 'items':
            self._return_items

    def __iter__(self):
        return self

    def _return_keys(self):
        return self._keys.pop()

    def _return_items(self):
        key=self._keys.pop()
        return key,self._redis_client.hget(self._name,self._keys.pop())

    def _return_values(self):
        return self._redis_client.hget(self._name,self._keys.pop())

    def next(self):
        if not self._keys:
            self._keys = self._redis_client.hkeys(self._name)
        if not self._keys:
            raise StopIteration
        if self._type == 'keys':
            return
        return self._ret_function()



class SessionStore(SessionBase):

    def delete(self, session_key=None):
        return self._redis_client.hdel(DJANGO_SESSION,session_key)



    def save(self, must_create=False):
        pass

    def create(self):
        pass

    def load(self):
        pass

    def __init__(self,session_key=None):
        super().__init__(session_key)
        host = getattr(settings, 'REDIS_HOST', None)
        port = getattr(settings, 'REDIS_PORT', None)
        name = getattr(settings, 'INSTANCE_NAME', str(uuid.uuid4()))
        self._redis_client = redis.StrictRedis(host=host, port=port)



    def decode(self, session_data):

        return super().decode(session_data)

    def has_key(self, key):
        return self._redis_client.hexists(DJANGO_SESSION,key)

    def delete_test_cookie(self):
        super().delete_test_cookie()

    def set_expiry(self, value):
        if not self._redis_client.hexists(DJANGO_SESSION,'_session_expiry'):
            return self._redis_client.hset(DJANGO_SESSION,'_session_expiry',value)
        else:
            return False

    def get(self, key, default=None):
        return self._redis_client.hget(DJANGO_SESSION,key)

    def keys(self):
        return self._redis_client.hkeys(DJANGO_SESSION)

    def cycle_key(self):
        super().cycle_key()

    def update(self, dict_):
        keys=dict_.keys()
        for key in keys:
            self._redis_client.hset(dict_[key])
        self.modified=True

    def get_expiry_age(self, **kwargs):
        return super().get_expiry_age(**kwargs)

    def is_empty(self):
        return super().is_empty()

    def itervalues(self):
        return RedisIterator(self._redis_client, 'values')

    def set_test_cookie(self):
        super().set_test_cookie()

    def test_cookie_worked(self):
        return super().test_cookie_worked()

    def get_expire_at_browser_close(self):
        return super().get_expire_at_browser_close()

    def items(self):
        return self._redis_client.hgetall(DJANGO_SESSION).items()

    def iteritems(self):
        return RedisIterator(self._redis_client,'items')

    def clear(self):
        super().clear()

    def encode(self, session_dict):
        return super().encode(session_dict)

    def flush(self):
        super().flush()

    def get_expiry_date(self, **kwargs):
        return super().get_expiry_date(**kwargs)


    def iterkeys(self):
        return RedisIterator(self._redis_client, 'keys')

    def setdefault(self, key, value):
        if self._redis_client.hsetnx(DJANGO_SESSION,key,value):
            return value
        else:
            return self.get(key=key)

    def values(self):
        return self.itervalues()

