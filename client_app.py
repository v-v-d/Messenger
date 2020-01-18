"""Messenger client side main script."""
import sys

from client import Client


server_address = None
server_port = None

try:
    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    if not 1024 < server_port < 65535:
        raise ValueError
except IndexError:
    print('Server host and port will be set by default.')
except ValueError:
    print('Port number must be in range 1024 - 65535.')
    sys.exit(1)

if server_address and server_port:
    client = Client(host=server_address, port=server_port)
else:
    client = Client()

client.run()
