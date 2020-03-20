"""Handlers for client side of Messenger app."""
from logging import getLogger
from logging.config import dictConfig

from log.log_config import LOGGING
from protocol import is_protocol_object_valid

dictConfig(LOGGING)
LOGGER = getLogger('client')


def handle_protocol_object(protocol_object, resolver, database):
    """
    Handle protocol object.
    :param (any) protocol_object: Response or local request.
    :return (any) : Returned object by controller.
    """
    if is_protocol_object_valid(protocol_object):
        action = protocol_object.get('action')
        controller = resolver(action)

        if controller:
            try:
                result = controller(protocol_object, database)
                LOGGER.debug(f'Controller {action} resolved with protocol object: {protocol_object}.')
                return result
            except Exception as error:
                LOGGER.error(f'Controller {action} rejected. Error: {error}')
        else:
            LOGGER.error(f'Controller {action} is not local or it\'s not supported.')
    else:
        LOGGER.error(f'Bad protocol object format: {protocol_object}')
