"""Server side utility functions for Messenger app."""
from argparse import ArgumentParser


def get_socket_parameters():
    """Get the server IP address and server listening port from command line."""
    socket_parameters = {
        'address': None,
        'port': None,
    }

    parser = ArgumentParser(description='Set the server IP address and server listening port.')
    parser.add_argument(
        '-a', '--address', type=str,
        required=False, help='Set server IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int,
        required=False, help='Set server listening port'
    )
    args = parser.parse_args()

    if args.address:
        socket_parameters['address'] = args.address
    if args.port:
        socket_parameters['port'] = args.port

    return socket_parameters
