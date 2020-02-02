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


def get_valid_parser(*args):
    """
    Get the server IP address and server listening port from command line.
    Address = '0.0.0.0' and port = 7777 is set by default.
    :param (Tuple) args: Tuple with arguments for command line parser.
    :return (argparse.Namespace): Namespace with socket parameters if port is valid, raise ValueError otherwise.
    """
    parser = parse_args(*args)
    if is_port_valid(parser.port):
        return parser
    else:
        raise ValueError(f'ValueError: port must be 1024-65536, {parser.port} given.')


def is_port_valid(port):
    """
    Validate port.
    :param (int) port: Server listening port.
    :return (bool): True if valid, False otherwise.
    """
    min_port_value = 1024
    max_port_value = 65536
    return min_port_value <= port <= max_port_value
