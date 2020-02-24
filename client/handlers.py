"""Handlers for client side of Messenger app."""
from logging import getLogger
from logging.config import dictConfig

from resolvers import get_controller, get_local_controller
from log.log_config import LOGGING
from protocol import is_response_valid, is_request_valid

dictConfig(LOGGING)
LOGGER = getLogger('client')


def handle_response(response):
    """
    Handle response from server.
    :param (any) response: Response from server.
    :return (any) : Returned object by controller.
    """
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
    else:
        LOGGER.error(f'Bad response format: {response}')


def handle_local_request(request):
    """
    Handle local request.
    :param (any) request: Local request.
    :return (<class 'function'>) : Controller associated with action passed in local request.
    """
    if is_request_valid(request):
        action = request.get('action')
        controller = get_local_controller(action)
        if controller:
            try:
                controller(request)
                LOGGER.debug(f'Controller {action} resolved with local request: {request}.')
                return controller
            except Exception as error:
                LOGGER.error(f'Controller {action} rejected. Error: {error}')
    else:
        LOGGER.error(f'Bad local request format: {request}')
