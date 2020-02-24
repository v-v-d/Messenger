from logging import getLogger
from logging.config import dictConfig

from resolver import get_controller
from log.log_config import LOGGING
from protocol import is_response_valid


dictConfig(LOGGING)
LOGGER = getLogger('client')


def handle_response(response):
    if is_response_valid(response):
        action = response.get('action')
        controller = get_controller(action)
        if controller:
            try:
                result = controller(response)
                LOGGER.debug(f'Controller {action} resolved with response: {response}.')
                return result
            except Exception as error:
                LOGGER.error(f'Controller {action} rejected. Error: {error}')
        else:
            LOGGER.error(f'Controller {action} not found.')
