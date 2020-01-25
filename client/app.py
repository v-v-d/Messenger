"""Client side Messenger app."""
import sys
import json
from logging import getLogger
from logging.config import dictConfig
from time import time
from socket import socket, AF_INET, SOCK_STREAM

from log.log_config import LOGGING


class Client:
    """Messenger client side main class."""
    def __init__(self, host='127.0.0.1', port=7777, buffersize=1024, name='Guest'):
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
        self.socket = socket(AF_INET, SOCK_STREAM)

        dictConfig(LOGGING)
        self.logger = getLogger('client')

    def run(self):
        """Run the client."""
        self.connect()
        self.write()
        self.read()
        self.socket.close()
        self.logger.info('Client shutdown.')

    def connect(self):
        """Connect to server with host and port attributes."""
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info(f'Client connected to server with {self.host}:{self.port}.')
        except ConnectionRefusedError as error:
            self.logger.critical(f'Connection closed. Error: {error}.')
            sys.exit(1)

    def write(self):
        """Send bytes request to server."""
        request = self.get_request()
        bytes_request = json.dumps(request).encode('UTF-8')
        self.socket.send(bytes_request)
        self.logger.debug(f'Client send request {request}.')

    def get_request(self):
        """Get request to server.
        :return (dict): Dict with request body.
        """
        return {
            'action': 'presence',
            'time': time(),
            'user': {
                'account_name': self.name
            }
        }

    def read(self):
        """Read response from server."""
        try:
            status_code = self.get_status_code()
            self.logger.debug(f'Response status code: {status_code}.')
        except (ValueError, json.JSONDecodeError):
            self.logger.critical('Failed to decode server response.')

    def get_status_code(self):
        """Get status code from server response.
        :return (str): Status code.
        """
        response = self.get_response()
        self.logger.debug(f'Client got response {response}.')
        if self.is_response_valid(response):
            return '200 : OK' if response.get('status') == 200 else f'400 : {response.get("error")}'

    def get_response(self):
        """Get decoded response from server.
        :return (dict): Dict with response body.
        """
        bytes_response = self.socket.recv(self.buffersize)
        return json.loads(bytes_response.decode('UTF-8'))

    @staticmethod
    def is_response_valid(response):
        """
        Validate response.
        :param (dict) response: Response from server.
        :return: True if response is valid, raise ValueError otherwise.
        """
        if 'status' in response:
            return True
        raise ValueError
