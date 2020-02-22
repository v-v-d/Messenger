"""Server side utility functions for Messenger app."""
from argparse import ArgumentParser
from collections import namedtuple


def parse_args(*args):
    """
    Create a command line argument parser and add arguments to it.
    :param (Tuple) args: Tuple with arguments for parser.
    :return (argparse.Namespace): Namespace with added arguments.
    """
    parser = ArgumentParser(description='Set up server parameters.')
    parser.add_argument(
        '-a', '--address', type=str, default='0.0.0.0',
        required=False, help='Set server IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=7777,
        required=False, help='Set server listening port'
    )
    parser.add_argument(
        '-m', '--migrate', action='store_true',
        required=False, help='Propagate changes into database'
    )
    return parser.parse_args(*args)


def get_socket_info(addr, port):
    Socket_info = namedtuple('Socket_info', ['addr', 'port'])
    return Socket_info(addr, port)
