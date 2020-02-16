"""Server side utility functions for Messenger app."""
from argparse import ArgumentParser


def parse_args(*args):
    """
    Create a command line argument parser and add arguments to it.
    :param (Tuple) args: Tuple with arguments for parser.
    :return (argparse.Namespace): Namespace with added arguments.
    """
    parser = ArgumentParser(description='Set the server IP address and server listening port.')
    parser.add_argument(
        '-a', '--address', type=str, default='0.0.0.0',
        required=False, help='Set server IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=7777,
        required=False, help='Set server listening port'
    )
    return parser.parse_args(*args)
