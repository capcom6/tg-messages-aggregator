import fastapi
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware

from .logging import setup_logging

server = fastapi.FastAPI(
    # docs_url="/docs" if config.common.debug else None,
    # redoc_url="/redoc" if config.common.debug else None,
)

server.add_middleware(GZipMiddleware, minimum_size=1024)


@server.get("/")
async def index(request: fastapi.Request):
    return {"a": "b"}
