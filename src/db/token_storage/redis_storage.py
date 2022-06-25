from datetime import timedelta
from typing import (
    Any,
    Optional,
)

from redis import StrictRedis

from db.token_storage.base import BaseTokenStorage


class RedisTokenStorage(BaseTokenStorage):
    def __init__(self, redis_host: str, redis_port: int) -> None:
        self.redis = StrictRedis(host=redis_host, port=redis_port, db=0)

    def get_value(self, key: str) -> Any:
        return self.redis.get(key)

    def set_value(self, key: str, token_value: Any, time_to_leave: Optional[timedelta] = None) -> None:
        self.redis.set(key, token_value, ex=time_to_leave)
