"""Protocol for server side of Messenger app."""
import json

from utils import get_socket_info


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
    if data:
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False
    return True


def make_response(request, code, data=None, r_addr=None, l_addr=None):
    """
    Make response based on passed request, status code and data.
    :param (dict) request: Dict from client with request body.
    :param (int) code: Status code.
    :param (str) data: Transmitted server data (message).
    :param (namedtuple) r_addr: Remote client address.
    :param (namedtuple) l_addr: Local client address.
    :return (dict) : Dict with response body.
    """
    if not r_addr:
        r_addr = get_socket_info_from_request(request, 'remote')
    if not l_addr:
        l_addr = get_socket_info_from_request(request, 'local')

    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code,
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


def get_socket_info_from_request(request, addr_type):
    socket_info = request.get('address')

    type_socket_info = socket_info.get(addr_type)
    addr, port = type_socket_info.get('addr'), type_socket_info.get('port')

    return get_socket_info(addr, port)
