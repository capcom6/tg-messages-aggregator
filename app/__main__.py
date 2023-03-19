if __name__ == "__main__":
    from app.cli import cli

    cli()

    # l = storage.lrange("accounts", 0, -1)
    # print(l)

    # a = Account.parse_raw(l[0])
    # print(repositories.AccountsRepository.select())

# import os
# from telethon import TelegramClient
# from telethon.errors.rpcerrorlist import SessionPasswordNeededError
# from teleredis import RedisSession
# from .config import config
# from .storage import storage
# from .logging import setup_logging
# import logging

# import asyncio


# async def main():
#     logging.debug(config)

#     phone = os.environ.get("USER_ID") or ""
#     password = os.environ.get("USER_SECRET") or ""

#     session = RedisSession(phone, storage)
#     client = TelegramClient(session, config.telegram.api_id, config.telegram.api_hash)

#     # 1. Запрашиваем код входа `await client.send_code_request(phone=phone)`
#     # 2. Входим `await client.sign_in` с кодом, если ловим `SessionPasswordNeededError`, то еще раз `await client.sign_in` с паролем
#     # 3. Далее достаточно `await client.connect()`

#     # await client.start(phone=lambda: phone, password=lambda: password)
#     await client.connect()
#     # print(await client.send_code_request(phone=phone))
#     # try:
#     #     await client.sign_in(
#     #         phone=phone,
#     #         code="31554",
#     #         phone_code_hash="dcd5ec885aa4993020",
#     #     )
#     # except SessionPasswordNeededError:
#     #     await client.sign_in(
#     #         phone=phone,
#     #         password=password,
#     #     )
#     try:
#         is_logged_in = await client.is_user_authorized()
#         if is_logged_in:
#             me = await client.get_me()
#             print(me.phone)

#         # await client.log_out()
#         pass
#     finally:
#         await client.disconnect()

#     return

#     async with TelegramClient("anon", api_id, api_hash) as client:
#         # Getting information about yourself
#         me = await client.get_me()

#         # "me" is a user object. You can pretty-print
#         # any Telegram object with the "stringify" method:
#         print(me.stringify())

#         # When you print something, you see a representation of it.
#         # You can access all attributes of Telegram objects with
#         # the dot operator. For example, to get the username:
#         username = me.username
#         print(username)
#         print(me.phone)

#         # You can print all the dialogs/conversations that you are part of:
#         # async for dialog in client.iter_dialogs():
#         #     print(dialog.name, "has ID", dialog.id)


# if __name__ == "__main__":
#     asyncio.run(main())
