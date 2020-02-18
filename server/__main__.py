"""Messenger server side main script."""
from logging import getLogger
from logging.config import dictConfig

from app import Server
from db.utils import migrate_db
from utils import parse_args
from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('server')

PARSER = parse_args()

if PARSER.migrate:
    migrate_db()
    LOGGER.debug('Migrations has been applied.')

try:
    with Server(host=PARSER.address, port=PARSER.port) as server:
        server.run()

except ValueError as error:
    LOGGER.critical(f'Can\'t run the server. Error: {error}')
