"""Protocol for server side of Messenger app."""


def is_request_valid(request):
    """
    Check for valid keys in request.
    :param (dict) request: Dict from client with request body.
    :return (bool) : True if all valid keys in request, False otherwise.
    """
    valid_keys = ('action', 'time', 'data', 'token', 'address')
    return all(key in request for key in valid_keys)


def make_response(request, code, data=None):
    """
    Make response based on passed request, status code and data.
    :param (dict) request: Dict from client with request body.
    :param (int) code: Status code.
    :param (str) data: Transmitted server data (message).
    :return (dict) : Dict with response body.
    """
    socket_info = request.get('address')
    remote_socket_info = socket_info.get('remote')
    local_socket_info = socket_info.get('local')

    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code,
        'address': {
            'remote': {
                'addr': remote_socket_info.get('addr'),
                'port': remote_socket_info.get('port'),
            },
            'local': {
                'addr': local_socket_info.get('addr'),
                'port': local_socket_info.get('port'),
            },
        },
    }
