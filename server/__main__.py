"""Messenger server side main script."""
from logging import getLogger
from logging.config import dictConfig

from app import Server
from db.database import migrate_db
from ui.app import GUIApplication
from utils import parse_args, get_config
from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('server')

PARSER = parse_args()

if PARSER.migrate:
    migrate_db()
    LOGGER.debug('Migrations has been applied.')

CONFIG = get_config(PARSER)

try:
    with Server(host=CONFIG.address, port=CONFIG.port) as server:
        server.daemon = True
        server.start()

        with GUIApplication() as gui:
            gui.render()

except ValueError as error:
    LOGGER.critical(f'Can\'t run the server. Error: {error}')
