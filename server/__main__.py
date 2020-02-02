"""Messenger server side main script."""
# Via terminal run 'python server' in root dir if you don't want to
# set up address and port. It will be set by default. Otherwise run
# 'python server -a 0.0.0.0 -p 8888' for example for set it up.
from logging import getLogger
from logging.config import dictConfig

from app import Server
from utils import get_valid_parser
from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('server')

try:
    PARSER = get_valid_parser()

    with Server(host=PARSER.address, port=PARSER.port) as server:
        server.run()

except ValueError as error:
    LOGGER.error(f'{error}.')
