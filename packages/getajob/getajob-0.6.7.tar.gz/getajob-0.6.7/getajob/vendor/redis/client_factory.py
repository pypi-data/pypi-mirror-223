import redis

from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockRedis


class RedisClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockRedis()

    @staticmethod
    def _return_client():
        return redis.Redis(
            host=SETTINGS.REDIS_HOST,
            port=SETTINGS.REDIS_PORT,
            password=SETTINGS.REDIS_PASSWORD,
            ssl=True,
        )
