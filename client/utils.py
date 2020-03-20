"""Client side utility functions for Messenger app."""
from argparse import ArgumentParser
from array import array
from collections import namedtuple
from itertools import islice
from logging import getLogger
from logging.config import dictConfig

from log.log_config import LOGGING

dictConfig(LOGGING)
LOGGER = getLogger('client')


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

    return parser.parse_args(*args)


PARSER = parse_args()


def make_presence_action_and_data(client_name):
    action = 'presence'
    data = {'client': client_name}
    return action, data


def set_socket_info(addr, port):
    Socket_info = namedtuple('Socket_info', ['addr', 'port'])
    return Socket_info(addr, port)


def get_chunk(text, size):
    """Get chunk and residue from received text."""
    text_iter = (char for char in text)
    chunk = array('B', islice(text_iter, size)).tobytes()
    text_residue = array('B', text_iter).tobytes()
    return chunk, text_residue
