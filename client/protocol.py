"""Protocol for client side of Messenger app."""
from time import time


def is_response_valid(response):
    """
    Check for valid keys in response.
    :param (dict) response: Dict from server with response body.
    :return (bool) : True if all valid keys in response, False otherwise.
    """
    valid_keys = ('action', 'time', 'data', 'code')
    if all(key in response for key in valid_keys):
        return True
    raise ValueError


def make_request(action, data, user):
    """
    Make request based on passed arguments and timestamp.
    :param (str) action: Protocol specially reserved action.
    The server will find a special way for response based on it.
    :param (str) data: Transmitted user data (message).
    :param (str) user: User who make the request.
    :return (dict) : Dict with request body.
    """
    return {
        'action': action,
        'time': time(),
        'data': data,
        'user': user,
    }
