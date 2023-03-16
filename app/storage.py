import redis
from .config import config


storage = redis.from_url(config.storage.dsn)
