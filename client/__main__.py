"""Messenger client side main script."""
# Via terminal run 'python client' in root dir if you don't want to set up address and port.
# It will be set by default. Otherwise run 'python client -a 0.0.0.0 -p 8888' for example for set it up.
from logging import getLogger
from logging.config import dictConfig

from app import Client
from utils import get_socket_params
from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('client')

try:
    SOCKET_PARAMS = get_socket_params()
    CLIENT = Client(host=SOCKET_PARAMS.address, port=SOCKET_PARAMS.port)
    CLIENT.run()
except ValueError as error:
    LOGGER.error(f'{error}.')
