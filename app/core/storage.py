import redis
import redis.asyncio as redis_aio
from ..config import config


storage = redis_aio.from_url(config.storage.dsn)
storage_sync = redis.from_url(config.storage.dsn)
