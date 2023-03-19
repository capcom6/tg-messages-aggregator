from dataclasses import dataclass

from .models import Account


@dataclass(frozen=True)
class Session:
    is_active: bool


@dataclass(frozen=True)
class AccountWithSession:
    account: Account
    session: Session
