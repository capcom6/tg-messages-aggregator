import asyncio
import functools
import os

import click

from .logging import setup_logging

setup_logging()


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--host", default="127.0.0.1", show_default=True, help="Hostname to listen on"
)
@click.option("--port", default=8000, show_default=True, help="Port to listen on")
def start(host: str, port: int):
    """Start the server"""
    import uvicorn

    uvicorn.run("app.api:server", host=host, port=port, reload=True)


@cli.command()
@make_sync
async def bot():
    """Start Telegram Bot"""
    from app.bot import run

    await run()
