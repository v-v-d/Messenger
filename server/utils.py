"""Server side utility functions for Messenger app."""
from argparse import ArgumentParser


def get_socket_parameters():
    """
    Get the server IP address and server listening port from command line.
    Address = '0.0.0.0' and port = 7777 set by default.
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
    args = parser.parse_args()
    if not 1024 <= args.port <= 65536:
        raise ValueError(f'ValueError: port must be 1024-65535, {args.port} given')
    return args
