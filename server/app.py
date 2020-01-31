"""Server side Messenger app."""
import json
from zlib import compress, decompress
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM

from log.log_config import LOGGING
from decorators import log


class Server:
    """Messenger server side main class."""
    def __init__(self, host='0.0.0.0', port=7777, backlog=5, bufsize=1024):
        """
        Server initialization.
        :param (str) host: Server IP address.
        :param (int) port: Server listening port.
        :param (int) backlog: The number of unaccepted connections that
        the system will allow before refusing new connections.
        :param (int) bufsize: The maximum amount of data to be received at once.
        """
        self.bufsize = bufsize
        self.backlog = backlog
        self.host = host
        self.port = port
        self.socket = None

        self._requests = list()
        self._connections = list()
        self._r_list = list()
        self._w_list = list()
        self._x_list = list()

        dictConfig(LOGGING)
        self.logger = getLogger('server')

    def __enter__(self):
        if not self.socket:
            self.socket = socket(AF_INET, SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Server shutdown'
        if exc_type and exc_type is not KeyboardInterrupt:
            message = 'Server stopped with error'
        self.logger.info(message, exc_info=exc_val)
        return True

    def run(self):
        """Run the server."""
        self.init_session()
        while True:
            client, address = self._accept_client()
            request = self.get_request(client)
            if request:
                self.logger.debug(f'Client {address[0]}:{address[1]} sent request: {request}')
                self.write(client, request)

    def init_session(self):
        """Session initialization by binding and listen to address."""
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(0)
        self.socket.listen(self.backlog)
        self.logger.info(f'Server was started with {self.host}:{self.port}.')

    def _accept_client(self):
        """
        Accept a connection from listening address and add it
        to connections list.
        :return (tuple): A pair (client, address) where client
        is a new client socket object usable to send and receive
        data, and address is the client address.
        """
        try:
            client, address = self.socket.accept()
        except OSError:
            pass
        else:
            self.logger.info(f'Client was connected with {address[0]}:{address[1]}.')
            self._connections.append(client)
            return client, address

    @log
    def get_request(self, client):
        """
        Get decoded and decompressed request from client.
        :param client: Client socket object.
        :return: Dict with client request body, None otherwise.
        """
        try:
            bytes_request = decompress(client.recv(self.bufsize))
            request = json.loads(bytes_request.decode('UTF-8'))
        except (ValueError, json.JSONDecodeError):
            self.logger.critical('Failed to decode client request.')
        else:
            return request if request else None

    def write(self, client, request):
        """Encode and compress response. Then send it to client.
        :param client: Client socket object.
        :param request: Dict with client request body.
        """
        response = self.make_response(request)
        self.logger.debug(f'Server make response: {response}')
        bytes_response = json.dumps(response).encode('UTF-8')
        client.send(compress(bytes_response))

    @log
    def make_response(self, request):
        """Make response based on request validation.
        :param request: Dict with client request body.
        :return: Dict with server response body.
        """
        if self.is_request_valid(request):
            return {'status': 200}
        else:
            return {
                'status': 400,
                'error': 'Bad Request',
            }

    @staticmethod
    def is_request_valid(request):
        """
        Validate request by checking keys and values existence.
        :param request: Dict with client request body.
        :return: True if request is valid, False otherwise.
        """
        if ('action' in request and request.get('action') == 'presence' and
                'time' in request and 'user' in request and
                request.get('user').get('account_name') == 'Guest'):
            return True
        else:
            return False
