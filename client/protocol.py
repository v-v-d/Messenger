"""Protocol for client side of Messenger app."""
import json
from time import time


def is_response_valid(response):
    """
    Check for valid keys in response.
    :param (dict) response: Dict from server with response body.
    :return (bool) : True if all valid keys in response, False otherwise.
    """
    valid_keys = ('action', 'time', 'data', 'code', 'address')
    if all(key in response for key in valid_keys):
        return True
    raise ValueError


def is_request_valid(request):
    """
    Check for valid keys in request.
    :param (dict) request: Dict from client with request body.
    :return (bool) : True if all valid keys in request, False otherwise.
    """
    valid_keys = ('action', 'time', 'data', 'token', 'address')
    is_keys_valid = all(key in request for key in valid_keys)

    return is_keys_valid and is_data_format_valid(request.get('data'))


def is_data_format_valid(data):
    """
    Validation request data filed format.
    :param (any) data: Request data filed body.
    :return (bool) : True if request data filed format valid, False otherwise.
    """
    if data:
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False
    return True


def make_request(action, data, r_addr, l_addr, token=None):
    """
    Make request based on passed arguments and timestamp.
    :param (str) action: Protocol specially reserved action.
    The server will find a special way for response based on it.
    :param (str) data: Transmitted user data (message).
    :param (namedtuple) r_addr: Remote client address.
    :param (namedtuple) l_addr: Local client address.
    :param (str) token: Client session token.
    :return (dict) : Dict with request body.
    """
    return {
        'action': action,
        'time': time(),
        'data': data,
        'token': token,
        'address': {
            'remote': {
                'addr': r_addr.addr,
                'port': r_addr.port,
            },
            'local': {
                'addr': l_addr.addr,
                'port': l_addr.port,
            },
        },
    }
