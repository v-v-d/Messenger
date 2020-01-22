"""Tests for client get_status_code Client class method."""
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


@pytest.fixture
def error_response_fixture():
    """Fixture with dict with error status in response body.
    :return (dict): Response with error status in body.
    """
    return {
        'status': 400,
        'error': 'Bad Request',
    }


@pytest.fixture
def ok_status_fixture():
    """Fixture with dict with 200 status in response body.
    :return (dict): Response with 200 status in body.
    """
    return '200 : OK'


@pytest.fixture
def error_status_fixture(error_response_fixture):
    """Fixture with dict with 200 status in response body.
    :return (dict): Response with 200 status in body.
    """
    return f'400 : {error_response_fixture.get("error")}'


def test_valid_get_status_code_ok(
        client_fixture, server_socket_fixture, server_address_fixture,
        server_port_fixture, ok_response_fixture, ok_status_fixture
):
    """
    Create server and client sockets then set it up for interaction. Send ok response from
    server socket and receive it from client socket. Get ok status code from server
    response and compare it with valid ok status.
    """
    try:
        server_socket_fixture.bind((server_address_fixture, server_port_fixture))
        server_socket_fixture.listen(5)

        client_fixture.connect()

        client, client_addr = server_socket_fixture.accept()

        bytes_response = json.dumps(ok_response_fixture).encode('UTF-8')
        client.send(bytes_response)

        assert client_fixture.get_status_code() == ok_status_fixture

    except Exception as error:
        raise AssertionError(f'Can\'t handle client-server application. Error: {error}')

    finally:
        server_socket_fixture.close()
        client_fixture.socket.close()


def test_valid_get_status_code_error(
        client_fixture, server_socket_fixture, server_address_fixture,
        server_port_fixture, error_response_fixture, error_status_fixture
):
    """
    Create server and client sockets then set it up for interaction. Send error response from
    server socket and receive it from client socket. Get error status code from server
    response and compare it with valid error status.
    """
    try:
        server_socket_fixture.bind((server_address_fixture, server_port_fixture))
        server_socket_fixture.listen(5)

        client_fixture.connect()

        client, client_addr = server_socket_fixture.accept()

        bytes_response = json.dumps(error_response_fixture).encode('UTF-8')
        client.send(bytes_response)

        assert client_fixture.get_status_code() == error_status_fixture

    except Exception as error:
        raise AssertionError(f'Can\'t handle client-server application. Error: {error}')

    finally:
        server_socket_fixture.close()
        client_fixture.socket.close()

# TODO: Try to refactoring duplicate code tests.
