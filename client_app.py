"""Messenger client side main script."""
import sys

from client import Client


SERVER_ADDRESS = None
SERVER_PORT = None

try:
    SERVER_ADDRESS = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    if not 1024 < SERVER_PORT < 65535:
        raise ValueError
except IndexError:
    print('Server host and port will be set by default.')
except ValueError:
    print('Port number must be in range 1024 - 65535.')
    sys.exit(1)

if SERVER_ADDRESS and SERVER_PORT:
    CLIENT = Client(host=SERVER_ADDRESS, port=SERVER_PORT)
else:
    CLIENT = Client()

CLIENT.run()
