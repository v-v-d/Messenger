"""Server side Messenger app."""
import json
from select import select
from zlib import compress, decompress
from logging import getLogger
from logging.config import dictConfig
from socket import socket, AF_INET, SOCK_STREAM

from log.log_config import LOGGING
from handler import handle_request
from decorators import log
from metaclasses import ServerVerifier
from descriptors import HostValidator, PortValidator, BufsizeValidator


class Server(metaclass=ServerVerifier):
    """Messenger server side main class."""
    host = HostValidator()
    port = PortValidator()
    bufsize = BufsizeValidator()

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
        if exc_type and exc_type is not KeyboardInterrupt:
            self.logger.critical(f'Server stopped with error: {exc_val}')
        else:
            self.logger.info('Server shutdown.')
        return True

    def run(self):
        """
        Initialize non-blocking session. Accept and handle
        clients. Read clients requests and write to them
        responses.
        """
        self.init_session()
        while True:
            self._accept_client()
            self._handle_clients()
            self._read()
            self._write()

    @log
    def init_session(self):
        """
        Non-blocking session initialization by binding and
        listen to socket.
        """
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(0)
        self.socket.listen(self.backlog)
        self.logger.info(f'Server was started with {self.host}:{self.port}.')

    def _accept_client(self):
        """
        Accept a connection from listening address and add it
        to connections list.
        """
        try:
            client, address = self.socket.accept()
            self.logger.info(f'Client was connected with {address[0]}:{address[1]}.')
            self._connections.append(client)
        except:
            pass

    def _handle_clients(self):
        """
        Try to handle clients using the select() method if connections
        exist. Existing connections checking needed only for Windows.
        _r_list: wait until ready for reading;
        _w_list: wait until ready for writing;
        _x_list: wait for an “exceptional condition”.
        """
        if self._connections:
            self._r_list, self._w_list, self._x_list = select(
                self._connections, self._connections, self._connections, 0
            )

    def _read(self):
        """
        Get request from each other client in read list and add it
        to requests list. Remove client from connections list if
        exception was caught.
        """
        for client in self._r_list:
            try:
                self.get_request(client)
            except (ValueError, json.JSONDecodeError):
                self.logger.critical('Failed to decode client request.')
            except:
                self._remove_client(client)

    def get_request(self, client):
        """
        Get decoded and decompressed request from client. Add it
        to requests list.
        :param (<class 'socket.socket'>) client: Client socket object.
        """
        bytes_request = decompress(client.recv(self.bufsize))
        request = json.loads(bytes_request.decode('UTF-8'))
        self.logger.debug(f'Client send request: {request}')
        self._requests.append(request)

    def _remove_client(self, client):
        """
        Remove client from connections list if client exist in it.
        :param (<class 'socket.socket'>) client: Client socket object.
        """
        if client in self._connections:
            host, port = client.getpeername()
            self.logger.info(f'Client {host}:{port} was disconnected.')
            self._connections.remove(client)

    def _write(self):
        """
        Check the requests list. If it's not empty make response,
        encode and compress it and try to send it to reached waiting
        client. Remove client from connections list if exception
        was caught.
        """
        if self._requests:
            request = self._requests.pop()

            if request.get('data'):
                request['data'] = json.loads(request.get('data'))   # TODO: Убрать после появления GUI
            remote_socket_info = request.get('address').get('remote')
            r_addr, r_port = remote_socket_info.get('addr'), remote_socket_info.get('port')

            response = handle_request(request)
            if response:
                for client in self._connections:
                    if client.getpeername() == (r_addr, r_port):
                        bytes_response = json.dumps(response).encode('UTF-8')
                        try:
                            client.send(compress(bytes_response))
                            self.logger.debug(f'Server make response: {response}.')

                        except:
                            self._remove_client(client)
