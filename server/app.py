"""Server side Messenger app."""
import asyncio
from logging import getLogger
from logging.config import dictConfig

from db.utils import remove_from_active_clients, clear_active_clients_list
from decorators import log
from handler import handle_request
from log.log_config import LOGGING
from utils import get_receiver_addr_and_port

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
        self.transport = transport
        peername = self.transport.get_extra_info('peername')
        self.logger.info(
            f'Client was connected with {peername[0]}:{peername[1]}.'
        )

        CONNECTIONS.update({
            peername: self.transport
        })

    def connection_lost(self, exc):
        peername = self.transport.get_extra_info('peername')
        self.logger.info(f'Client {peername[0]}:{peername[1]} was disconnected.')

        if peername in CONNECTIONS:
            CONNECTIONS.pop(peername)
            remove_from_active_clients(peername[0], peername[1])

    def data_received(self, bytes_request):
        if not bytes_request:
            raise BytesWarning

        self.logger.debug(f'Client send request.')
        response = handle_request(bytes_request)

        if response:
            self._send_response(response)

    def _send_response(self, response):
        # TODO: респонс не отправляется получателю, только текущему сокету
        self._write_to_client(response, self.transport)

        receiver = get_receiver_addr_and_port(response)
        receiver_transport = CONNECTIONS.get(receiver)

        self.logger.info(f'************ sender: {self.transport.get_extra_info("peername")}')
        self.logger.info(f'************ receiver: {receiver}')

        if all((
            receiver != self.transport.get_extra_info('peername'),
            receiver_transport
        )):
            self._write_to_client(response, receiver_transport)

    def _write_to_client(self, response, client):
        client.write(response)
        self.logger.debug('Server make response.')
