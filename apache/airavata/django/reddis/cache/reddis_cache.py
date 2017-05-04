from django.core.cache.backends.base import BaseCache,DEFAULT_TIMEOUT
from django.conf import settings
import redis
import uuid

REDIS_CACHE_NAME="redis_cache"

class ReddisCache(BaseCache):

    def __init__(self,params):

        super(ReddisCache,self).__init__(params)
        host=getattr(settings,'REDIS_HOST',None)
        port=getattr(settings,'REDIS_PORT',None)
        name=getattr(settings,'INSTANCE_NAME',str(uuid.uuid4()))
        self._redis_client=redis.StrictRedis(host=host,port=port)


    def make_key(self, key, version=None):
        return super(ReddisCache, self).make_key()

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        gen_key=self.make_key(key,version)
        return self._redis_client.hset(REDIS_CACHE_NAME,gen_key,value,px=self.get_backend_timeout(timeout))

    def get(self, key, default=None, version=None):
        return self._redis_client.hget(REDIS_CACHE_NAME,self.make_key(key,version))

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
       return self.add(key,value,timeout=DEFAULT_TIMEOUT,version=None)

    def delete(self, key, version=None):
        return self._redis_client.hdelete(REDIS_CACHE_NAME,self.make_key(key,version))

    def has_key(self, key, version=None):
        return self._redis_client.exists(REDIS_CACHE_NAME,self.make_key(key,version))

    def incr(self, key, delta=1, version=None):
        return self._redis_client.append(REDIS_CACHE_NAME,self.make_key(key,version),delta)

    def clear(self):
        keys=self._redis_client.keys(pattern=self._name+'.*')
        for key in keys:
            self.delete(key)









