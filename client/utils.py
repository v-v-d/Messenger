"""Client side utility functions for Messenger app."""
from argparse import ArgumentParser


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
    return parser.parse_args(*args)
