"""Client side utility functions for Messenger app."""
from argparse import ArgumentParser


def parse_args(*args):
    """
    Create a command line argument parser and add arguments to it.
    :param (Tuple) args: Tuple with arguments for parser.
    :return (argparse.Namespace): Namespace with added arguments.
    """
    parser = ArgumentParser(description='Set the client IP address and server listening port.')
    parser.add_argument(
        '-a', '--address', type=str, default='localhost',
        required=False, help='Set client IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=7777,
        required=False, help='Set server listening port'
    )
    return parser.parse_args(*args)


def get_socket_params(*args):
    """
    Get the client IP address and server listening port from command line.
    Address = 'localhost' and port = 7777 is set by default.
    :param (Tuple) args: Tuple with arguments for command line parser.
    :return (argparse.Namespace): Namespace with socket parameters if port is valid, raise ValueError otherwise.
    """
    parser = parse_args(*args)
    if is_port_valid(parser.port):
        return parser
    else:
        raise ValueError(f'ValueError: port must be 1024-65535, {parser.port} given.')


def is_port_valid(port):
    """
    Validate port.
    :param (int) port: Server listening port.
    :return (bool): True if valid, False otherwise.
    """
    return 1024 <= port <= 65536
