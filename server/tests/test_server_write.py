"""Tests for server write Server class method."""
import json
from time import time
from zlib import decompress
from socket import socket, AF_INET, SOCK_STREAM

import pytest

from app import Server


@pytest.fixture
def client_address_fixture():
    """Client address fixture.
    :return (str): Client address.
    """
    return 'localhost'


@pytest.fixture
def server_port_fixture():
    """Server listening port fixture.
    :return (int): Server listening port.
    """
    return 8080


@pytest.fixture
def server_address_fixture():
    """Server address fixture.
    :return (str): Server address.
    """
    return '0.0.0.0'


@pytest.fixture
def server_fixture(server_address_fixture, server_port_fixture):
    """Server instance fixture.
    :return (<class 'app.Server'>): Server instance object.
    """
    return Server(host=server_address_fixture, port=server_port_fixture)


@pytest.fixture
def request_fixture():
    """Valid request fixture.
    :return (dict): Dict with valid request.
    """
    return {
        'action': 'presence',
        'time': time(),
        'user': {
            'account_name': 'Guest'
        }
    }


def test_valid_write(
        server_fixture, server_address_fixture, server_port_fixture,
        client_address_fixture, request_fixture
):
    """
    Create client socket and get Server instance then set them up for interaction.
    Make response from server based on request fixture, send it and receive it on
    client socket. Then check that response have 200 status code.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        server_fixture.socket.bind((server_address_fixture, server_port_fixture))
        server_fixture.socket.listen(5)

        client_socket.connect((client_address_fixture, server_port_fixture))

        client, client_addr = server_fixture.socket.accept()
        server_fixture.write(client, request_fixture)

        response_from_server = json.loads(decompress(client_socket.recv(1024)).decode('UTF-8'))

        assert response_from_server.get('status') == 200

    except Exception as error:
        raise AssertionError(f'Can\'t handle client-server application. Error: {error}')

    finally:
        server_fixture.socket.close()
        client_socket.close()
