"""Protocol for client side of Messenger app."""
from time import time


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
