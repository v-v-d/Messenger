"""Handler for server side of Messenger app."""
from logging import getLogger
from logging.config import dictConfig

from clients_db import is_client_in_db
from log.log_config import LOGGING
from protocol import is_request_valid, make_response

dictConfig(LOGGING)
LOGGER = getLogger('server')


def handle_request(request):
    """
    Get response by handling client request.
    :param (any) request: Request from client.
    :return (dict) : Dict with response body.
    """
    try:
        if is_request_valid(request):
            action = request.get('action')
            if is_action_valid(action):
                to_client = request.get('data').get('to_user')
                if is_client_in_db(to_client):
                    data = get_response_data(request)
                    response = make_response(request, 200, data)
                else:
                    message = f'Can\'t send message to {to_client}. User with this name does not exist.'
                    response = make_response(request, 404, message)
                    LOGGER.error(message)
            else:
                response = make_response(request, 404, f'Action "{action}" not supported.')
                LOGGER.error(f'Action "{action}" not found.')
        else:
            response = make_response(request, 400, 'Bad Request.')
            LOGGER.error(f'Wrong request: {request}')

    except Exception as error:
        response = make_response(request, 500, 'Internal server error.')
        LOGGER.critical(f'Internal server error: {error}')

    return response


def is_action_valid(action):
    """
    Validate action.
    :param (str) action: Action name from client request.
    :return (bool) : True if action is valid, False otherwise.
    """
    valid_actions = (
        'presence',
        'echo',
    )
    return action in valid_actions


def get_response_data(request):
    """
    Get response data based on request action name.
    :param (dict) request: Dict with client request body.
    :return (str) : Data to client.
    """
    action = request.get('action')
    client = request.get('user')

    if action == 'presence':
        data = f'{client}, welcome to messenger!'
    else:
        text = request.get('data').get('text')
        data = f'{client}: {text}'

    return data
