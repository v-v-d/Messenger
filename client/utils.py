"""Client side utility functions for Messenger app."""
import json
import zlib
from argparse import ArgumentParser
from collections import namedtuple

from protocol import make_request


def parse_args(*args):
    """
    Create a command line argument parser and add arguments to it.
    :param (Tuple) args: Tuple with arguments for parser.
    :return (argparse.Namespace): Namespace with added arguments.
    """
    parser = ArgumentParser(description='Set the client parameters')
    parser.add_argument(
        '-a', '--address', type=str, default='127.0.0.1',
        required=False, help='Set client IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=7777,
        required=False, help='Set server listening port'
    )
    parser.add_argument(
        '-n', '--name', type=str, default='Guest',
        required=False, help='Set username'
    )
    parser.add_argument(
        '-m', '--migrate', action='store_true',
        required=False, help='Propagate changes into database'
    )

    return parser.parse_args(*args)


PARSER = parse_args()


def make_presence_message(socket, r_addr, l_addr, client_name):
    """Send presence message for identify client on the server side."""
    data = json.dumps({'client': client_name})  # TODO: Убрать json.dumps() после появления GUI
    request = make_request(
        action='presence',
        data=data,
        r_addr=r_addr,
        l_addr=l_addr,
    )
    bytes_request = json.dumps(request).encode('UTF-8')
    socket.send(zlib.compress(bytes_request))


def set_socket_info(addr, port):
    Socket_info = namedtuple('Socket_info', ['addr', 'port'])
    return Socket_info(addr, port)
