import asyncio
import contextlib
from teleredis import RedisSession
from telethon import TelegramClient, sessions
from telethon.errors.rpcerrorlist import SessionPasswordNeededError

from app.config import config
from app.core.channels import AccountsUpdatedChannel
from app.core.domain import AccountWithSession, Session
from app.core.errors import SessionAlreadyActiveError
from app.core.models import Account
from app.core.repositories import AccountsRepository, SessionsRepository


class AccountsService:
    @classmethod
    async def select(cls) -> list[Account]:
        return await AccountsRepository.select()

    @classmethod
    async def get(cls, phone: str) -> AccountWithSession | None:
        account = await AccountsRepository.get(phone=phone)
        if not account:
            return None

        return AccountWithSession(
            account=account,
            session=Session(await SessionsRepository.is_exists(phone=phone)),
        )

    @classmethod
    async def insert(cls, account: Account) -> bool:
        return await AccountsRepository.insert(account=account)

    @classmethod
    async def delete(cls, phone: str):
        await cls.session_delete(phone)
        await AccountsRepository.delete(phone=phone)

    @classmethod
    async def session_init(cls, phone: str) -> str:
        is_active = await SessionsRepository.is_exists(phone=phone)
        if is_active:
            raise SessionAlreadyActiveError

        session = await cls.session_get(phone)
        async with cls._tg_client(session) as client:
            req = await client.send_code_request(phone=phone)
        return req.phone_code_hash

    @classmethod
    async def session_confirm(
        cls, request_id: str, phone: str, code: str, *, password: str | None
    ):
        session = await cls.session_get(phone)
        async with cls._tg_client(session) as client:
            try:
                await client.sign_in(
                    phone=phone,
                    code=code,
                    phone_code_hash=request_id,
                )
            except SessionPasswordNeededError:
                if password:
                    await client.sign_in(
                        phone=phone,
                        password=password,
                    )
                else:
                    raise

        await AccountsUpdatedChannel.notify(phone)

    @classmethod
    async def session_get(cls, phone: str):
        return await SessionsRepository.get(phone)

    @classmethod
    async def session_delete(cls, phone: str):
        session = await cls.session_get(phone)
        async with cls._tg_client(session) as client:
            await client.log_out()
        if await SessionsRepository.delete(phone):
            await AccountsUpdatedChannel.notify(phone)

    @classmethod
    @contextlib.asynccontextmanager  # type: ignore
    async def _tg_client(cls, session: sessions.Session):
        client = TelegramClient(
            session=session,
            api_id=config.telegram.api_id,
            api_hash=config.telegram.api_hash,
        )
        await client.connect()

        yield client

        await client.disconnect()  # type: ignore
        # await asyncio.wait_for(client.disconnect(), None)
        # await client.run_until_disconnected()
