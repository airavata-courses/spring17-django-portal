import django.core.cache.backends.memcached.MemcachedCache
from django.core.cache.backends.base import BaseCache,DEFAULT_TIMEOUT
import redis
import uuid

class ReddisCache(BaseCache):

    def __init__(self,params,host,port,name):
        super(ReddisCache,self).__init__(params)
        self._redis_client=redis.StrictRedis(host=host,port=port)
        if name:
            self._name=name
        else:
            self._name=str(uuid.uuid4())


    def make_key(self, key, version=None):
        return self._name + ":"+super(ReddisCache, self).make_key()

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        gen_key=self.make_key(key,version)
        return self._redis_client.set(gen_key,value,px=self.get_backend_timeout(timeout))

    def get(self, key, default=None, version=None):
        return self._redis_client.get(self.make_key(key,version))

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
       return self.add(key,value,timeout=DEFAULT_TIMEOUT,version=None)

    def delete(self, key, version=None):
        return self._redis_client.delete(self.make_key(key,version))

    def has_key(self, key, version=None):
        return self._redis_client.exists(self.make_key(key,version))

    def incr(self, key, delta=1, version=None):
        return self._redis_client.append(self.make_key(key,version),delta)

    def clear(self):
        keys=self._redis_client.keys(pattern=self._name+'.*')
        for key in keys:
            self.delete(key)









