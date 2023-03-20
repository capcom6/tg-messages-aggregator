import asyncio
import logging

from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import SessionExpiredError, PhoneNumberBannedError
from app.core.channels import AccountsUpdatedChannel
from app.core.services import AccountsService
from app.config import config


clients: dict[str, TelegramClient] = {}


async def listen_events():
    async for m in AccountsUpdatedChannel.listen():
        logging.info(m)
        phone = m["data"]
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

    clients[phone] = client


async def start_clients():
    accounts = await AccountsService.select()
    for account in accounts:
        details = await AccountsService.get(account.phone)
        if not details or not details.session.is_active:
            continue
        await start_client(account.phone)


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
