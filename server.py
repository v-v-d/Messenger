"""Server side Messenger app."""
import json
from socket import socket, AF_INET, SOCK_STREAM


class Server:
    """Messenger server side main class."""
    def __init__(self, host='0.0.0.0', port=7777, max_connections=5, buffersize=1024):
        """
        Server initialization.
        :param (str) host: Server IP address.
        :param (int) port: Server port number.
        :param (int) max_connections: Max connections queue.
        :param (int) buffersize: TCP max data size in bytes.
        """
        self.buffersize = buffersize
        self.max_connections = max_connections
        self.host = host
        self.port = port
        self._socket = socket(AF_INET, SOCK_STREAM)

    def run(self):
        """Run the server."""
        self._init_session()
        while True:
            client, address = self._socket.accept()
            request = self._get_request(client)
            if request:
                print(f'Client {address[0]}:{address[1]} sent request: {request}')
                self._write(client, request)

    def _init_session(self):
        """Session initialization by binding and listening socket."""
        self._socket.bind((self.host, self.port))
        self._socket.listen(self.max_connections)
        print(f'Server was started with {self.host}:{self.port}.')

    def _get_request(self, client):
        """
        Get decoded request from client.
        :param client: Client socket object.
        :return: Dict with client request body, None otherwise.
        """
        try:
            bytes_request = client.recv(self.buffersize)
            request = json.loads(bytes_request.decode('UTF-8'))
        except (ValueError, json.JSONDecodeError):
            print(f'Failed to decode client request.')
        else:
            return request if request else None

    def _write(self, client, request):
        """Send response to client.
        :param client: Client socket object.
        :param request: Dict with client request body.
        """
        response = self._make_response(request)
        bytes_response = json.dumps(response).encode('UTF-8')
        client.send(bytes_response)

    def _make_response(self, request):
        """Make response based on request validation.
        :param request: Dict with client request body.
        :return: Dict with server response body.
        """
        if self._is_valid(request):
            return {'status': 200}
        else:
            return {
                'status': 400,
                'error': 'Bad Request',
            }

    @staticmethod
    def _is_valid(request):
        """
        Validate request.
        :param request: Dict with client request body.
        :return: True if request is valid, False otherwise.
        """
        if ('action' in request and request['action'] == 'presence' and
                'time' in request and 'user' in request and
                request['user']['account_name'] == 'Guest'):
            return True
        else:
            return False
