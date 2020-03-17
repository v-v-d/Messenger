"""Client side of Messenger app."""
import json
import zlib
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from db.local_storage import LocalStorage
from handlers import handle_protocol_object
from log.log_config import LOGGING
from protocol import is_response_valid, make_request
from decorators import log
from descriptors import PortValidator, HostValidator, BufsizeValidator
from metaclasses import ClientVerifier
from resolvers import get_local_request_controller, get_response_controller
from utils import make_presence_action_and_data, set_socket_info


class Client(Thread, metaclass=ClientVerifier):
    """Messenger client side main class."""
    host = HostValidator()
    port = PortValidator()
    bufsize = BufsizeValidator()

    def __init__(self, host='127.0.0.1', port=7777, bufsize=1024, client_name=None):
        """
        Client initialization.
        :param (str) host: Server IP address.
        :param (int) port: Server listening port.
        :param (int) bufsize: The maximum amount of data to be received at once.
        """
        super().__init__()
        self.bufsize = bufsize
        self.host = host
        self.port = port
        self.client_name = client_name
        self.socket = None
        self.token = None
        self._r_addr = None
        self._l_addr = None
        self.database = None

        dictConfig(LOGGING)
        self.logger = getLogger('client')

    def __enter__(self):
        if not self.socket:
            self.socket = socket(AF_INET, SOCK_STREAM)
        if self.client_name:
            self.database = LocalStorage(self.client_name)
            self.database.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown.'
        if exc_type and exc_type is not KeyboardInterrupt:
            message = f'Client stopped with error: {exc_type}: {exc_val}.'
        self.logger.info(message)
        return True

    def run(self):
        """Run the client."""
        self.connect()
        self.read()

    @log
    def connect(self):
        """Connect to server with host and port attributes."""
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info(f'Client connected to server with {self.host}:{self.port}.')

            self._set_addresses()
            self.write(*make_presence_action_and_data(self.client_name))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError) as error:
            self.logger.critical(f'Connection closed. Error: {error}.')

    def _set_addresses(self):
        self._r_addr = set_socket_info(*self.socket.getsockname())
        self._l_addr = set_socket_info(self.host, self.port)

    def write(self, action, data):
        """Send compressed bytes request to server."""
        try:
            request = self.get_request(action, data)
            local_response = handle_protocol_object(
                request, get_local_request_controller, self.database
            )

            if not local_response:
                bytes_request = json.dumps(request).encode('UTF-8')
                self.socket.send(zlib.compress(bytes_request))
                self.logger.debug(f'Client send request {request}.')
            else:
                return local_response

        except Exception as error:
            self.logger.critical(f'Can\'t send request. Error: {error}')

    def get_request(self, action, data):
        """Get request to server.
        :return (dict): Dict with request body.
        """
        return make_request(
            action=action,
            data=json.dumps(data),
            r_addr=self._r_addr,
            l_addr=self._l_addr,
            token=self.token
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
                data = handle_protocol_object(response, get_response_controller, self.database)
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
        if token and not self.token:
            self.token = token
