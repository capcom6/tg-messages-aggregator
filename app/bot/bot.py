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
            # await clients[phone].disconnect()
            # del clients[phone]

        logging.warning("Start client!")
        asyncio.create_task(start_client(phone))
        # await start_client(phone)


async def start_client(phone: str):
    session = await AccountsService.session_get(phone)

    client = TelegramClient(session, config.telegram.api_id, config.telegram.api_hash)

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        try:
            print(event)
            # print(f"New message from {account.phone}: {event.message.message}")
            notify_message = f"New message from {phone}: {event.message.message}"
            # notify_account_id = notify_account_ids[i]
        # обрабатываем полученное сообщение и отправляем уведомление через Телеграм-бот
        except SessionExpiredError:
            # обработка ошибки, если сессия аккаунта пользователя истекла
            print("Сессия пользователя истекла")
            notify_message = "Сессия пользователя истекла"
        except PhoneNumberBannedError:
            # обработка ошибки, если аккаунт пользователя заблокирован
            print("Аккаунт пользователя заблокирован")
            notify_message = "Аккаунт пользователя заблокирован"
        except Exception as e:
            # обработка других ошибок
            print(f"Произошла ошибка: {e}")
            notify_message = f"Произошла ошибка: {e}"
        finally:
            print(notify_message)
            # if notify_message:
            #     await bot_client.send_message(notify_account_id, notify_message)

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
        await start_clients()
        await listen_events()
    finally:
        for client in clients.values():
            try:
                client.disconnect()
                logging.info("Disconnected")
            except Exception as e:
                print(e)
        logging.info("Done")
