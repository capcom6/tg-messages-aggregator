from dataclasses import dataclass

from pydantic import Field
from app.core.domain import Session

from app.core.models import Account


@dataclass
class GetAccountResponse:
    account: Account
    session: Session


@dataclass
class PostAccountSessionResponse:
    request_id: str
