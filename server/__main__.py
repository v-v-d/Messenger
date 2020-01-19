"""Messenger server side main script."""
from app import Server
from utils import get_socket_parameters


# Run the file via command line with 'python .' if you don't want to set up address and port.
# It will be set by default. Otherwise run 'python . -a 0.0.0.0 -p 8888' for example for set up it.
SOCKET_PARAMETERS = get_socket_parameters()
ADDRESS = SOCKET_PARAMETERS['address']
PORT = SOCKET_PARAMETERS['port']

if ADDRESS and PORT:
    SERVER = Server(host=ADDRESS, port=PORT)
else:
    print('Server host and port will be set by default.')
    SERVER = Server()

SERVER.run()
