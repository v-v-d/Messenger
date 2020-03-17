"""Messenger client side main script."""
from logging import getLogger
from logging.config import dictConfig

from app import Client
from db.clients_db import migrate_db
from db.utils import get_active_client_name_from_clients_db
from log.log_config import LOGGING
from ui.app import GUIApplication
from utils import PARSER

dictConfig(LOGGING)
LOGGER = getLogger('client')

HOST, PORT = PARSER.address, PARSER.port

migrate_db()

NAME = get_active_client_name_from_clients_db()

try:
    with Client(host=HOST, port=PORT, client_name=NAME) as client:
        client.daemon = True
        client.start()

        with GUIApplication(client) as gui:
            gui.render()

except ValueError as error:
    LOGGER.critical(f'Can\'t run the client. Error: {error}')
