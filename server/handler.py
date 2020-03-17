"""Request handler for server side of Messenger app."""
import json
from logging import getLogger
from logging.config import dictConfig

from log.log_config import LOGGING
from protocol import is_request_valid, make_response
from resolver import get_controller
from security import encryption_middleware

dictConfig(LOGGING)
LOGGER = getLogger('server')


@encryption_middleware
def handle_request(request):
    """
    Get response by handling client request.
    :param (any) request: Request from client.
    :return (dict) : Dict with response body.
    """
    if is_request_valid(request):
        if request.get('data'):
            request['data'] = json.loads(request.get('data'))

        action = request.get('action')
        controller = get_controller(action)
        if controller:
            try:
                response = controller(request)
                LOGGER.debug(f'Controller {action} resolved with request: {request}')
            except Exception as error:
                response = make_response(request, 500, 'Internal server error.')
                LOGGER.critical(f'Controller {action} rejected. Error: {error.__class__}: {error}')
        else:
            response = make_response(request, 404, f'Action "{action}" not supported.')
            LOGGER.error(f'Controller {action} not found.')
    else:
        response = make_response(request, 400, 'Bad request format.')
        LOGGER.error(f'Bad request format: {request}')

    return response
