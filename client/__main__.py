"""Messenger client side main script."""
# Via terminal run 'python client' in root dir if you don't want to set up address and port.
# It will be set by default. Otherwise run 'python client -a 0.0.0.0 -p 8888' for example for set it up.
from app import Client
from utils import get_socket_parameters


try:
    SOCKET_PARAMETERS = get_socket_parameters()
    CLIENT = Client(host=SOCKET_PARAMETERS.address, port=SOCKET_PARAMETERS.port)
    CLIENT.run()
except ValueError as error:
    print(error)
