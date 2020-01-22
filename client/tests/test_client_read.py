"""Tests for client read Client class method."""
import json
from socket import socket, AF_INET, SOCK_STREAM

import pytest

from app import Client


@pytest.fixture
def client_fixture(client_address_fixture, server_port_fixture):
    """Client instance fixture.
    :return (Client): Client instance.
    """
    return Client(host=client_address_fixture, port=server_port_fixture)


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
def server_socket_fixture():
    """Server socket fixture.
    :return (socket.socket): Server socket object.
    """
    return socket(AF_INET, SOCK_STREAM)


@pytest.fixture
def ok_response_fixture():
    """Fixture with dict with 200 status in response body.
    :return (dict): Response with 200 status in body.
    """
    return {'status': 200}


def test_valid_read(
        client_fixture, server_socket_fixture,server_address_fixture,
        server_port_fixture, ok_response_fixture):
    """
    Create server and client sockets then set it up for interaction. Send test dict from
    server socket and receive it from client socket. Then check that method get no exceptions.
    """
    try:
        server_socket_fixture.bind((server_address_fixture, server_port_fixture))
        server_socket_fixture.listen(5)

        client_fixture.connect()

        client, client_addr = server_socket_fixture.accept()

        bytes_response = json.dumps(ok_response_fixture).encode('UTF-8')
        client.send(bytes_response)

        assert client_fixture.read() is None

    except Exception as error:
        raise AssertionError(f'Can\'t handle client-server application. Error: {error}')

    finally:
        server_socket_fixture.close()
        client_fixture.socket.close()
