from .singleton import singleton
import os
import redis


@singleton
class RedisService:

    def __init__(self, **kwargs):
        self.connection = self.connect(**kwargs)

    def connect(self, **kwargs):
        redis_con = redis.StrictRedis(host=kwargs["host"], port=kwargs["port"], password=kwargs["passwd"])

        return redis_con

    def set(self, key, value):
        self.connection.set(key, value)

    def get(self, key):
        value = self.connection.get(key)
        return value

    def disconnect(self):
        self.connection.close()


con = RedisService(host=os.getenv("REDIS_HOST"),
                   port=os.getenv("REDIS_PORT"),
                   passwd=os.getenv("REDIS_PASSWORD"),
                   )
