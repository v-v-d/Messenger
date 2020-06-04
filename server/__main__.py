"""Messenger server side main script."""
import asyncio
from logging import getLogger
from logging.config import dictConfig
from threading import Thread

from app import Server
from db.database import migrate_db
from descriptors import HostValidator, PortValidator
from log.log_config import LOGGING
from ui.app import GUIApplication
from utils import parse_args, get_config

dictConfig(LOGGING)
LOGGER = getLogger('server')


class ServerMeta:
    host = HostValidator()
    port = PortValidator()

    def __init__(self, host, port):
        self.host = host
        self.port = port


async def run_server_coro(host, port):
    """Run async server"""
    loop = asyncio.get_event_loop()
    server = await loop.create_server(
        Server, host, port
    )

    LOGGER.info(f'Server was started with {host}:{port}.')

    async with server:
        await server.serve_forever()


def run_async_server(host, port):
    asyncio.run(run_server_coro(host, port))


PARSER = parse_args()

if PARSER.migrate:
    migrate_db()
    LOGGER.debug('Migrations has been applied.')

CONFIG = get_config(PARSER)

server_meta = ServerMeta(CONFIG.address, CONFIG.port)

Thread(
    target=run_async_server, args=(server_meta.host, server_meta.port),
    daemon=True, name='server'
).start()

with GUIApplication() as gui:
    gui.render()
