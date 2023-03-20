import asyncio
from app.core.storage import storage


class AccountsUpdatedChannel:
    KEY = "accounts:updated"

    @classmethod
    async def notify(cls, phone: str):
        await storage.publish(cls.KEY, phone)

    @classmethod
    async def listen(cls):
        channel = storage.pubsub()
        await channel.subscribe(cls.KEY)
        try:
            while True:
                if message := await channel.get_message(True):
                    yield message
                await asyncio.sleep(1)
        finally:
            await channel.close()
