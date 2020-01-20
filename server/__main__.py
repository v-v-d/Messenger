"""Messenger server side main script."""
# Via terminal run 'python server' in root dir if you don't want to set up address and port.
# It will be set by default. Otherwise run 'python server -a 0.0.0.0 -p 8888' for example for set it up.
from app import Server
from utils import get_socket_params


try:
    SOCKET_PARAMS = get_socket_params()
    SERVER = Server(host=SOCKET_PARAMS.address, port=SOCKET_PARAMS.port)
    SERVER.run()
except ValueError as error:
    print(error)
