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
        :param (int) port: Server listening port.
        :param (int) buffersize: TCP max data size in bytes.
        :param (str) name: Username.
        """
        self.buffersize = buffersize
        self.host = host
        self.port = port
        self.name = name
        self.socket = socket(AF_INET, SOCK_STREAM)

    def run(self):
        """Run the client."""
        self.connect()
        self.write()
        self.read()
        self.socket.close()

    def connect(self):
        """Connect to server with host and port attributes."""
        self.socket.connect((self.host, self.port))

    def write(self):
        """Send bytes request to server."""
        bytes_request = json.dumps(self.get_request()).encode('UTF-8')
        self.socket.send(bytes_request)

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
            print(status_code)
        except (ValueError, json.JSONDecodeError):
            print('Failed to decode server response.')

    def get_status_code(self):
        """Get status code from server response.
        :return (str): Status code.
        """
        response = self.get_response()
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
