import asyncio
import logging

from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import (
    SessionExpiredError,
    PhoneNumberBannedError,
    UnauthorizedError,
)
from app.core.channels import AccountsUpdatedChannel
from app.core.services import AccountsService
from app.config import config


bot = TelegramClient("bot", config.telegram.api_id, config.telegram.api_hash)
clients: dict[str, TelegramClient] = {}


async def listen_events():
    async for m in AccountsUpdatedChannel.listen():
        logging.info(m)
        phone = m["data"]
        await asyncio.sleep(1)
        details = await AccountsService.get(phone)
        logging.info(details)
        if not details or not details.session.is_active:
            if phone in clients:
                await clients[phone].disconnect()
                del clients[phone]
            continue
        if phone in clients:
            continue

        logging.warning("Start client!")
        asyncio.create_task(start_client(phone))
        # await start_client(phone)


async def start_client(phone: str):
    session = await AccountsService.session_get(phone)

    client = TelegramClient(session, config.telegram.api_id, config.telegram.api_hash)
    bot_id = (await bot.get_me()).id
    print(bot_id)

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        try:
            if event.message.peer_id.user_id == bot_id:
                print("From bot")
                return

            print(event.message.peer_id.user_id)
            notify_message = f"New message from {phone}: {event.message.message}"
        except Exception as e:
            # обработка других ошибок
            print(f"Произошла ошибка: {e}")
            notify_message = f"Произошла ошибка: {e}"

        print(notify_message)
        if notify_message:
            await bot.send_message(config.bot.destination, notify_message)

    await client.connect()

    if not await client.is_user_authorized():
        logging.warning(f"Client {phone} is not authorized")
        await AccountsService.session_delete(phone)
        await client.disconnect()
        return

    logging.info("Connected")
    clients[phone] = client

    try:
        await client.run_until_disconnected()
    except UnauthorizedError as e:
        await AccountsService.session_delete(phone)
        logging.error(e)
    except Exception as e:
        logging.warning(e)

    del clients[phone]
    logging.info("Disconnected")


async def start_clients():
    accounts = await AccountsService.select()
    for account in accounts:
        details = await AccountsService.get(account.phone)
        if not details or not details.session.is_active:
            continue

        asyncio.create_task(start_client(account.phone))

        logging.info("Next")


async def run():
    # asyncio.create_task()
    try:
        await bot.start(bot_token=config.bot.token)
        await start_clients()
        await listen_events()
    finally:
        for client in clients.values():
            try:
                client.disconnect()
                logging.info("Disconnected")
            except Exception as e:
                print(e)
        try:
            await bot.disconnect()
        except Exception as e:
            print(e)
        logging.info("Done")
