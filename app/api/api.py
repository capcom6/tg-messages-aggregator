import fastapi
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware

from app.core.errors import SessionAlreadyActiveError

from .requests import PatchAccountSessionRequest, PostAccountRequest
from .responses import GetAccountResponse, PostAccountSessionResponse

import app.core.models as models
from app.core.services import AccountsService

server = fastapi.FastAPI(
    # docs_url="/docs" if config.common.debug else None,
    # redoc_url="/redoc" if config.common.debug else None,
)

server.add_middleware(GZipMiddleware, minimum_size=1024)


@server.get("/api/account")
async def get_accounts():
    return {"accounts": await AccountsService.select()}


@server.get("/api/account/{phone}", response_model=GetAccountResponse)
async def get_account(phone: str):
    account = await AccountsService.get(phone=phone)
    if not account:
        raise fastapi.HTTPException(404)
    return {"account": account.account, "session": account.session}


@server.post("/api/account")
async def post_account(account: PostAccountRequest):
    if not await AccountsService.insert(account=models.Account.parse_obj(account)):
        raise fastapi.HTTPException(409)
    return fastapi.responses.Response(status_code=201)


@server.delete("/api/account/{phone}")
async def delete_account(phone: str):
    await AccountsService.delete(phone=phone)
    return fastapi.responses.Response(status_code=204)


@server.post("/api/account/{phone}/session")
async def post_account_session(phone: str) -> PostAccountSessionResponse:
    try:
        return PostAccountSessionResponse(
            request_id=await AccountsService.session_init(phone=phone)
        )
    except SessionAlreadyActiveError:
        raise fastapi.HTTPException(409)


@server.patch("/api/account/{phone}/session")
async def patch_account_session(phone: str, body: PatchAccountSessionRequest):
    await AccountsService.session_confirm(
        body.request_id, phone, body.code, password=body.password
    )


@server.delete("/api/account/{phone}/session", status_code=204)
async def delete_account_session(phone: str):
    await AccountsService.session_delete(phone)
