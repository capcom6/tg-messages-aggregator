import fastapi
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware

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


@server.get("/api/account/{phone}")
async def get_account(phone: str):
    account = await AccountsService.get(phone=phone)
    if not account:
        raise fastapi.HTTPException(404)
    return {"account": account}


@server.post("/api/account")
async def post_account(account: models.Account):
    if not await AccountsService.insert(account=account):
        raise fastapi.HTTPException(409)
    return fastapi.responses.Response(status_code=201)


@server.delete("/api/account/{phone}")
async def delete_account(phone: str):
    await AccountsService.delete(phone=phone)
    return fastapi.responses.Response(status_code=204)
