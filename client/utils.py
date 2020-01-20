"""Client side utility functions for Messenger app."""
from argparse import ArgumentParser, ArgumentError


def get_socket_parameters():
    """
    Get the client IP address and server listening port from command line.
    Address = 'localhost' and port = 7777 set by default.
    """
    parser = ArgumentParser(description='Set the client IP address and server listening port.')
    parser.add_argument(
        '-a', '--address', type=str, default='0.0.0.0',
        required=False, help='Set client IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=7777,
        required=False, help='Set server listening port'
    )
    return parser.parse_args()
