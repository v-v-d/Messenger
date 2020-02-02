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
        '-a', '--address', type=str, default='localhost',
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


def get_valid_parser(*args):
    """
    Get the client IP address and server listening port from command line.
    Address = 'localhost' and port = 7777 is set by default.
    :param (Tuple) args: Tuple with arguments for command line parser.
    :return (argparse.Namespace): Namespace with socket parameters if port is valid, raise ValueError otherwise.
    """
    parser = parse_args(*args)
    if is_parser_valid(parser):
        return parser
    raise ValueError(f'Error: port must be 1024-65536, {parser.port} given.')


def is_parser_valid(parser):
    """
    Validate parser.
    :param (argparse.Namespace) parser: Parser namespace.
    :return (bool): True if valid, False otherwise.
    """
    min_port_value = 1024
    max_port_value = 65536
    return min_port_value <= parser.port <= max_port_value
