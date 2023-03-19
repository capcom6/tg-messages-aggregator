import redis.asyncio as redis
from ..config import config


storage = redis.from_url(config.storage.dsn)
