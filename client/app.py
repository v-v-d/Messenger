"""Client side Messenger app."""
import json
from zlib import compress, decompress
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM

from log.log_config import LOGGING
from protocol import is_response_valid, make_request
from decorators import log


class Client:
    """Messenger client side main class."""
    def __init__(self, host='127.0.0.1', port=7777, buffersize=1024, name='Guest', mode='recv'):
        """
        Client initialization.
        :param (str) host: Client IP address.
        :param (int) port: Server listening port.
        :param (int) buffersize: TCP max data size in bytes.
        :param (str) name: Username.
        """
        self.buffersize = buffersize
        self.host = host
        self.port = port
        self.name = name
        self.socket = None

        dictConfig(LOGGING)
        self.logger = getLogger('client')

        self.mode = mode

    def __enter__(self):
        if not self.socket:
            self.socket = socket(AF_INET, SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown.'
        if exc_type and exc_type is not KeyboardInterrupt:
            message = f'Client stopped with error: {exc_val}'
        self.logger.info(message)
        return True

    def run(self):
        """Run the client."""
        self.connect()

        if self.mode == 'send':
            self.write()

        elif self.mode == 'recv':
            self.read()

    def connect(self):
        """Connect to server with host and port attributes."""
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info(f'Client connected to server with {self.host}:{self.port}.')
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as error:
            self.logger.critical(f'Connection closed. Error: {error}.')

    @log
    def write(self):
        """Send bytes request to server."""
        request = self.get_request()
        bytes_request = json.dumps(request).encode('UTF-8')
        self.socket.send(compress(bytes_request))
        self.logger.debug(f'Client send request {request}.')

    def get_request(self):
        """Get request to server.
        :return (dict): Dict with request body.
        """
        action = input('action: ')
        data = input('data: ')
        return make_request(action, data, self.name)

    @log
    def read(self):
        """Read response from server."""
        try:
            response = self.get_response()
            self.logger.debug(f'Client got response: {response}.')

            data = response.get('data')
            print(f'{data.get("user")}: {data.get("text")}')
        except (ValueError, json.JSONDecodeError):
            self.logger.critical('Failed to decode server response.')

    def get_response(self):
        """Get decoded response from server.
        :return (dict): Dict with response body.
        """
        bytes_response = decompress(self.socket.recv(self.buffersize))
        response = json.loads(bytes_response.decode('UTF-8'))
        if is_response_valid(response):
            return response
