from typing import Any
import abc
import json
import redis
from settings import base as base_settings


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RedisClient(metaclass=SingletonMeta):
    def __new__(cls, host: str, port: int, db: int):
        return redis.Redis(host=host, port=port, db=db)


class CacheService(metaclass=abc.ABCMeta):
    def __init__(self, client):
        self.client = client

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def set(self):
        pass


class RedisCacheService(CacheService):
    def get(self, key) -> Any:
        result = self.client.get(key)
        return json.loads(result.decode()) if result else None

    def set(self, key, value) -> bool:
        return self.client.set(key, value)

    def setnx(self, key, value) -> bool:
        return self.client.setnx(key, value)


redis_client = RedisClient(
    host=base_settings.REDIS_HOST,
    port=base_settings.REDIS_PORT,
    db=base_settings.REDIS_DB
)

cache_service = RedisCacheService(redis_client)
