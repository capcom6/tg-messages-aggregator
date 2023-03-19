import asyncio
from app.core.storage import storage


class AccountsUpdatedChannel:
    KEY = "accounts:updated"

    @classmethod
    async def notify(cls):
        await storage.publish(cls.KEY, "updated")

    @classmethod
    async def listen(cls):
        channel = storage.pubsub()
        await channel.subscribe(cls.KEY)
        try:
            while True:
                if message := await channel.get_message(True):
                    yield message
                await asyncio.sleep(1)
                # try:
                #     if message := await (
                #         await asyncio.wait_for(
                #             asyncio.get_event_loop().run_in_executor(
                #                 None, channel.get_message
                #             ),
                #             timeout=1.0,
                #         )
                #     ):
                #         if message["type"] == "message":
                #             yield message
                # except asyncio.TimeoutError:
                #     pass
                # finally:
                #     await asyncio.sleep(1)
        except KeyboardInterrupt:
            return
