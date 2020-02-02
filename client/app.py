"""Client side of Messenger app."""
import json
import zlib
from time import sleep
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, enumerate

from log.log_config import LOGGING
from protocol import is_response_valid, make_request
from decorators import log


class Client:
    """Messenger client side main class."""
    def __init__(self, host='127.0.0.1', port=7777, bufsize=1024, name='Guest'):
        """
        Client initialization.
        :param (str) host: Client IP address.
        :param (int) port: Server listening port.
        :param (int) bufsize: The maximum amount of data to be received at once.
        :param (str) name: Username.
        """
        self.bufsize = bufsize
        self.host = host
        self.port = port
        self.name = name
        self.socket = None

        dictConfig(LOGGING)
        self.logger = getLogger('client')

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
        self.write()
        self.read()
        self.check_threads_health()

    @log
    def connect(self):
        """Connect to server with host and port attributes."""
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info(f'Client connected to server with {self.host}:{self.port}.')
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as error:
            self.logger.critical(f'Connection closed. Error: {error}.')

    def write(self):
        """Start writer thread for sending requests to server."""
        Thread(target=self.start_writing, daemon=True, name='writer').start()

    def start_writing(self):
        """Send compressed bytes request to server."""
        while True:
            try:
                request = self.get_request()
                bytes_request = json.dumps(request).encode('UTF-8')
                self.socket.send(zlib.compress(bytes_request))
                self.logger.debug(f'Client send request {request}.')

            except Exception as error:
                self.logger.critical(f'Can\'t send request. Error: {error}')
                break

    def get_request(self):
        """Get request to server.
        :return (dict): Dict with request body.
        """
        action = input('action: ')
        data = input('data: ')
        return make_request(action, data, self.name)

    def read(self):
        """Start reader thread for reading responses from server."""
        Thread(target=self.start_reading, daemon=True, name='reader').start()

    def start_reading(self):
        """Read response from server."""
        while True:
            try:
                response = self.get_response()
                self.logger.debug(f'Client got response: {response}.')
                self.print_message(response)

            except (ValueError, json.JSONDecodeError):
                self.logger.critical('Failed to decode server response.')

            except Exception as error:
                self.logger.critical(f'Can\'t read response. Error: {error}')
                break

    def get_response(self):
        """Get decompressed and decoded response from server.
        :return (dict): Dict with response body.
        """
        bytes_response = zlib.decompress(self.socket.recv(self.bufsize))
        response = json.loads(bytes_response.decode('UTF-8'))
        if is_response_valid(response):
            return response

    @staticmethod
    def print_message(response):
        """
        Print message from user or error message from server.
        :param (dict) response: Dict with response body.
        """
        data = response.get('data')
        code = response.get('code')

        if isinstance(data, dict):
            message = f'\n{data.get("user")}: {data.get("text")}'
        else:
            message = f'\n{code}: {data}'

        print(message)

    @staticmethod
    def check_threads_health():
        """Reader and writer threads health checking."""
        current_th_names = [thread.name for thread in enumerate()]
        th_names = ('reader', 'writer')

        while True:
            sleep(1)
            if all(th_name in current_th_names for th_name in th_names):
                continue
            break
