import asyncio
from app.core.channels import AccountsUpdatedChannel


async def listen_events():
    async for m in AccountsUpdatedChannel.listen():
        print(m)


async def run():
    # asyncio.create_task()
    await listen_events()
