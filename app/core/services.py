import contextlib
from telethon import TelegramClient
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
        result = await AccountsRepository.insert(account=account)
        if result:
            await AccountsUpdatedChannel.notify()
        return result

    @classmethod
    async def delete(cls, phone: str):
        await SessionsRepository.delete(phone=phone)
        await AccountsRepository.delete(phone=phone)
        await AccountsUpdatedChannel.notify()

    @classmethod
    async def session_init(cls, phone: str) -> str:
        is_active = await SessionsRepository.is_exists(phone=phone)
        if is_active:
            raise SessionAlreadyActiveError

        session = await SessionsRepository.get(phone)
        async with cls._tg_client(session) as client:
            req = await client.send_code_request(phone=phone)
        return req.phone_code_hash

    @classmethod
    async def session_confirm(
        cls, request_id: str, phone: str, code: str, *, password: str | None
    ):
        session = await SessionsRepository.get(phone)
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

        await AccountsUpdatedChannel.notify()

    @classmethod
    async def session_delete(cls, phone: str):
        session = await SessionsRepository.get(phone)
        async with cls._tg_client(session) as client:
            await client.log_out()
        await SessionsRepository.delete(phone)

        await AccountsUpdatedChannel.notify()

    @classmethod
    @contextlib.asynccontextmanager  # type: ignore
    async def _tg_client(cls, session):
        client = TelegramClient(
            session=session,
            api_id=config.telegram.api_id,
            api_hash=config.telegram.api_hash,
        )
        await client.connect()

        yield client

        await client.disconnect()  # type: ignore
