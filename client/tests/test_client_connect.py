"""Tests for client connect Client class method."""
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


def test_valid_connect(client_fixture, server_socket_fixture, server_address_fixture, server_port_fixture):
    """
    Create server and client sockets then set it up for interaction. Send test dict from client
    socket and receive it from server socket. Then check that the two dict is the same.
    """
    try:
        server_socket_fixture.bind((server_address_fixture, server_port_fixture))
        server_socket_fixture.listen(5)

        client_fixture.connect()

        request_to_server = {'test': 'test'}
        bytes_request = json.dumps(request_to_server).encode('UTF-8')
        client_fixture.socket.send(bytes_request)

        client, client_addr = server_socket_fixture.accept()
        bytes_request_from_client = client.recv(1024)
        request_from_client = json.loads(bytes_request_from_client.decode('UTF-8'))

        return request_to_server == request_from_client

    except Exception as error:
        raise AssertionError(f'Can\'t handle client-server application. Error: {error}')

    finally:
        server_socket_fixture.close()
        client_fixture.socket.close()
