"""Server side Messenger app."""
import json
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM

from log.log_config import LOGGING


class Server:
    """Messenger server side main class."""
    def __init__(self, host='0.0.0.0', port=7777, max_connections=5, buffersize=1024):
        """
        Server initialization.
        :param (str) host: Server IP address.
        :param (int) port: Server listening port.
        :param (int) max_connections: Max connections queue.
        :param (int) buffersize: TCP max data size in bytes.
        """
        self.buffersize = buffersize
        self.max_connections = max_connections
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

        dictConfig(LOGGING)
        self.logger = getLogger('server')

    def run(self):
        """Run the server."""
        self.init_session()
        while True:
            client, address = self.socket.accept()
            self.logger.info(f'Client was connected with {address[0]}:{address[1]}.')
            request = self.get_request(client)
            if request:
                self.logger.debug(f'Client {address[0]}:{address[1]} sent request: {request}')
                self.write(client, request)

    def init_session(self):
        """Session initialization by binding and listening socket."""
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connections)
        self.logger.info(f'Server was started with {self.host}:{self.port}.')

    def get_request(self, client):
        """
        Get decoded request from client.
        :param client: Client socket object.
        :return: Dict with client request body, None otherwise.
        """
        try:
            bytes_request = client.recv(self.buffersize)
            request = json.loads(bytes_request.decode('UTF-8'))
        except (ValueError, json.JSONDecodeError):
            self.logger.critical('Failed to decode client request.')
        else:
            return request if request else None

    def write(self, client, request):
        """Send response to client.
        :param client: Client socket object.
        :param request: Dict with client request body.
        """
        response = self.make_response(request)
        self.logger.debug(f'Server make response: {response}')
        bytes_response = json.dumps(response).encode('UTF-8')
        client.send(bytes_response)

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
        Validate request.
        :param request: Dict with client request body.
        :return: True if request is valid, False otherwise.
        """
        if ('action' in request and request.get('action') == 'presence' and
                'time' in request and 'user' in request and
                request.get('user').get('account_name') == 'Guest'):
            return True
        else:
            return False
