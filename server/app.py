"""Server side Messenger app."""
import asyncio
from logging import getLogger
from logging.config import dictConfig

import handler
from db.utils import remove_from_active_clients, clear_active_clients_list
from decorators import log
from log.log_config import LOGGING

CONNECTIONS = {}


class Server(asyncio.Protocol):
    """Messenger server side main class with async."""

    def __init__(self):
        self.transport = None

        clear_active_clients_list()

        dictConfig(LOGGING)
        self.logger = getLogger('server')

    @log
    def connection_made(self, transport):
        """Called when a connection is made.

        The argument is the transport representing the pipe connection.
        To receive data, wait for data_received() calls.
        When the connection is closed, connection_lost() is called.
        """
        self.transport = transport
        peername = self.transport.get_extra_info('peername')
        self.logger.info(
            f'Client was connected with {peername[0]}:{peername[1]}.'
        )

        CONNECTIONS.update({
            peername: self.transport
        })

    def connection_lost(self, exc):
        """Called when the connection is lost or closed.

        The argument is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """
        peername = self.transport.get_extra_info('peername')
        self.logger.info(f'Client {peername[0]}:{peername[1]} was disconnected.')

        if peername in CONNECTIONS:
            CONNECTIONS.pop(peername)
            remove_from_active_clients(peername[0], peername[1])

    def data_received(self, bytes_request):
        """
        Called when some data is received.
        The argument is a bytes object.
        """
        if not bytes_request:
            raise BytesWarning

        self.logger.debug(f'Client send request.')
        bytes_response = handler.handle_request(bytes_request)

        if bytes_response:
            self.send_response(bytes_response)

    def send_response(self, bytes_response):
        """
        Get all receivers and send bytes response to them.
        :param bytes_response: compressed and encrypted bytes response
        """
        receiver_peername = handler.RECEIVER
        receiver_transport = CONNECTIONS.get(receiver_peername)

        if all((
            receiver_peername != self.transport.get_extra_info('peername'),
            receiver_transport
        )):
            self.write_to_client(bytes_response, receiver_transport)

        self.write_to_client(bytes_response, self.transport)

    def write_to_client(self, bytes_response, client):
        """
        Send bytes response to client network interface.
        :param bytes_response: compressed and encrypted bytes response
        :param client: client network interface
        """
        client.write(bytes_response)
        self.logger.debug('Server make response.')
