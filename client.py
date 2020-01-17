"""Client side Messenger app."""
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM


class Client:
    """Messenger client side main class."""
    def __init__(self, host='127.0.0.1', port=7777, buffersize=1024, name='Guest'):
        """
        Client initialization.
        :param (str) host: Client IP address.
        :param (int) port: Client port number.
        :param (int) buffersize: TCP max data size in bytes.
        :param (str) name: Username.
        """
        self.buffersize = buffersize
        self.host = host
        self.port = port
        self.name = name
        self._socket = socket(AF_INET, SOCK_STREAM)

    def run(self):
        """Run the client."""
        self._connect()
        self._write()
        self._read()
        self._socket.close()

    def _connect(self):
        """Connect to server with host and port attributes."""
        self._socket.connect((self.host, self.port))

    def _write(self):
        """Send bytes request to server."""
        bytes_request = json.dumps(self._get_request()).encode('UTF-8')
        self._socket.send(bytes_request)

    def _get_request(self):
        """Get request to server.
        :return: Dict with request body.
        """
        return {
            'action': 'presence',
            'time': time(),
            'user': {
                'account_name': self.name
            }
        }

    def _read(self):
        """Read response from server."""
        try:
            status_code = self._get_status_code()
            print(status_code)
        except (ValueError, json.JSONDecodeError):
            print('Failed to decode server message.')

    def _get_status_code(self):
        """Get status code from server response.
        :return: Status code.
        """
        response = self._get_response()
        if self._is_valid(response):
            return '200 : OK' if response['status'] == 200 else f'400 : {response["error"]}'

    @staticmethod
    def _is_valid(response):
        """
        Validate response.
        :param (dict) response: Response from server.
        :return: True if response is valid, raise ValueError otherwise.
        """
        if 'status' in response:
            return True
        else:
            raise ValueError

    def _get_response(self):
        """Get decoded response from server.
        :return: Dict with response body.
        """
        bytes_response = self._socket.recv(self.buffersize)
        return json.loads(bytes_response).decode('UTF-8')
