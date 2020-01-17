"""Client side Messenger app."""
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM


class Client:
    """Messenger client side main class."""
    def __init__(self, host='127.0.0.1', port=7777, buffersize=1024, name='Guest'):
        """
        Client initialization.
        :param (str) host: Client IPv4 address.
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
        """Get request to server."""
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
            print('Не удалось декодировать сообщение сервера.')

    def _get_status_code(self):
        """Get status code from server response."""
        response = self._get_response()
        if 'status' in response:
            if response['status'] == 200:
                return '200 : OK'
            return f'400 : {response["error"]}'
        raise ValueError

    def _get_response(self):
        """Get decoded response from server."""
        bytes_response = self._socket.recv(self.buffersize)
        return json.loads(bytes_response).decode('UTF-8')
