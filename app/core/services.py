from app.core.models import Account
from app.core.repositories import AccountsRepository
from app.core.channels import AccountsUpdatedChannel


class AccountsService:
    @classmethod
    async def select(cls) -> list[Account]:
        return await AccountsRepository.select()

    @classmethod
    async def get(cls, phone: str) -> Account | None:
        return await AccountsRepository.get(phone=phone)

    @classmethod
    async def insert(cls, account: Account) -> bool:
        result = await AccountsRepository.insert(account=account)
        if result:
            await AccountsUpdatedChannel.notify()
        return result

    @classmethod
    async def delete(cls, phone: str):
        await AccountsRepository.delete(phone=phone)
        await AccountsUpdatedChannel.notify()
