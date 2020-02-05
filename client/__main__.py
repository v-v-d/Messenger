"""Messenger client side main script."""
# Via terminal run 'python client' in root dir if you don't want to set up address and port.
# It will be set by default. Otherwise run 'python client -a 0.0.0.0 -p 8888' for example for set it up.
from logging import getLogger
from logging.config import dictConfig

from app import Client
from utils import get_valid_parser
from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('client')

try:
    PARSER = get_valid_parser()
    HOST, PORT, NAME = PARSER.address, PARSER.port, PARSER.name

    with Client(host=HOST, port=PORT, name=NAME) as client:
        client.run()

except ValueError as error:
    LOGGER.error(f'{error}.')
