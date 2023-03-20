import teleredis
import app.core.models as models
from .storage import storage, storage_sync


class AccountsRepository:
    KEY = "accounts"

    @classmethod
    async def select(cls) -> list[models.Account]:
        data = await storage.hvals(cls.KEY)
        return [models.Account.parse_raw(v) for v in data]

    @classmethod
    async def get(cls, phone: str) -> models.Account | None:
        data = await storage.hget(cls.KEY, phone)
        if not data:
            return None
        return models.Account.parse_raw(data)

    @classmethod
    async def insert(cls, account: models.Account) -> bool:
        return await storage.hsetnx(cls.KEY, account.phone, account.json()) == 1

    @classmethod
    async def delete(cls, phone: str):
        await storage.hdel(cls.KEY, phone)


class SessionsRepository:
    KEY = teleredis.teleredis.DEFAULT_HIVE_PREFIX

    @classmethod
    async def is_exists(cls, phone: str) -> bool:
        keys = await storage.keys(f"{cls.KEY}:{phone}:*")
        return len(keys) > 1

    @classmethod
    async def get(cls, phone: str):
        return teleredis.RedisSession(phone, storage_sync)

    @classmethod
    async def delete(cls, phone: str) -> bool:
        keys = await storage.keys(f"{cls.KEY}:{phone}:*")
        if len(keys) == 0:
            return False
        return await storage.delete(*keys) > 0
