"""Messenger client side main script."""
from logging import getLogger
from logging.config import dictConfig

from app import Client
from db.database import migrate_db
from utils import PARSER
from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('client')

if PARSER.migrate:
    migrate_db()
    LOGGER.debug('Migrations has been applied.')

HOST, PORT, NAME = PARSER.address, PARSER.port, PARSER.name

try:
    with Client(host=HOST, port=PORT, name=NAME) as client:
        client.run()

except ValueError as error:
    LOGGER.critical(f'Can\'t run the client. Error: {error}')
