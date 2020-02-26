"""Client side of Messenger app."""
import json
import zlib
from time import sleep
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, enumerate

from handlers import handle_response, handle_local_request
from log.log_config import LOGGING
from protocol import is_response_valid, make_request
from decorators import log
from descriptors import PortValidator, HostValidator, BufsizeValidator
from metaclasses import ClientVerifier
from utils import make_presence_message, set_socket_info


class Client(metaclass=ClientVerifier):
    """Messenger client side main class."""
    host = HostValidator()
    port = PortValidator()
    bufsize = BufsizeValidator()

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
        self._token = None
        self._r_addr = None
        self._l_addr = None

        dictConfig(LOGGING)
        self.logger = getLogger('client')

    def __enter__(self):
        if not self.socket:
            self.socket = socket(AF_INET, SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown.'
        if exc_type and exc_type is not KeyboardInterrupt:
            message = f'Client stopped with error: {exc_type}: {exc_val}'
        self.logger.info(message)
        return True

    def run(self):
        """Run the client."""
        self.connect()
        self.read()
        self.write()
        self.check_threads_health()

    @log
    def connect(self):
        """Connect to server with host and port attributes."""
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info(f'Client connected to server with {self.host}:{self.port}.')

            self._set_addresses()
            make_presence_message(self.socket, self._r_addr, self._l_addr, self.name)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as error:
            self.logger.critical(f'Connection closed. Error: {error}.')

    def _set_addresses(self):
        self._r_addr = set_socket_info(*self.socket.getsockname())
        self._l_addr = set_socket_info(self.host, self.port)

    def write(self):
        """Start writer thread for sending requests to server."""
        Thread(target=self.start_writing, daemon=True, name='writer').start()

    def start_writing(self):
        """Send compressed bytes request to server."""
        while True:
            try:
                request = self.get_request()

                if not handle_local_request(request):
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
        action = input('enter action: ')
        data = input('enter data: ')

        return make_request(
            action=action,
            data=data,
            r_addr=self._r_addr,
            l_addr=self._l_addr,
            token=self._token
        )

    def read(self):
        """Start reader thread for reading responses from server."""
        Thread(target=self.start_reading, daemon=True, name='reader').start()

    def start_reading(self):
        """Read response from server."""
        while True:
            try:
                response = self.get_response()
                self.logger.debug(f'Client got response: {response}.')
                data = handle_response(response)
                if data:
                    self._set_token(data)

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

    def _set_token(self, data):
        token = data.get('token')
        if token and not self._token:
            self._token = token

    @staticmethod
    def check_threads_health():    # TODO: выглядит костыльно, переделать
        """Reader and writer threads health checking."""
        current_th_names = [thread.name for thread in enumerate()]
        th_names = ('reader', 'writer')

        while True:
            sleep(1)    # TODO: выглядит костыльно, переделать
            if all(th_name in current_th_names for th_name in th_names):
                continue
            break
