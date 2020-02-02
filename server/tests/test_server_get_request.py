"""Tests for server get_request Server class method."""
import json
from time import time
from zlib import compress
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
    host = server_address_fixture
    port = server_port_fixture
    with Server(host=host, port=port) as server_socket:
        return server_socket


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


def test_valid_get_request(
        server_fixture, server_address_fixture, server_port_fixture,
        client_address_fixture, request_fixture
):
    """
    Create client socket and get Server instance then set them up for interaction.
    Send request from client and get it on server. Then check that they are equal.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        server_fixture.socket.bind((server_address_fixture, server_port_fixture))
        server_fixture.socket.listen(5)

        client_socket.connect((client_address_fixture, server_port_fixture))

        client, client_addr = server_fixture.socket.accept()

        client_socket.send(compress(json.dumps(request_fixture).encode('UTF-8')))

        request_from_server = server_fixture.get_request(client)

        assert request_from_server == request_fixture

    except Exception as error:
        raise AssertionError(f'Can\'t handle client-server application. Error: {error}')

    finally:
        server_fixture.socket.close()
        client_socket.close()
