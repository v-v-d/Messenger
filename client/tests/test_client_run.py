import json
from zlib import compress, decompress
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

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


def put_func_return_into_queue(queue, func, *args):
    """
    Put value into the queue. Value is the func returned value.
    :param (<class 'queue.Queue'>) queue: Queue object with passed func returned value.
    :param (<class 'function'>) func: Function whose returned value is passed in queue.
    :param (any) args: Arguments for passed func.
    """
    queue.put(func(*args))


def run_server(server_address, server_port):
    """
    Create server socket that accepted clients in endless cycle. Create response based
    on request and send it to client if client is accepted. Then return response value.
    :param (str) server_address: Server IP address.
    :param (int) server_port: Listening server port number.
    :return (dict): Dict object with response body.
    """
    server_socket = socket(AF_INET, SOCK_STREAM)

    try:
        server_socket.bind((server_address, server_port))
        server_socket.listen(5)

        while True:
            client, client_addr = server_socket.accept()

            try:
                request = json.loads(decompress(client.recv(1024)).decode('UTF-8'))

            except Exception as error:
                raise AssertionError('Recv server error: ', error)

            else:
                if request:
                    if ('action' in request and request.get('action') == 'presence' and
                            'time' in request and 'user' in request and
                            request.get('user').get('account_name') == 'Guest'):
                        response = {'status': 200}
                    else:
                        response = {
                            'status': 400,
                            'error': 'Bad Request',
                        }

                    client.send(compress(json.dumps(response).encode('UTF-8')))
                    return response

    except Exception as error:
        raise AssertionError('Server error: ', error)

    finally:
        server_socket.close()


def test_valid_run(client_fixture):
    """
    Test the client run method. Connect the server through
    a neighboring thread, get the result of the server response
    and compare it with the known values of the request keys.
    :param (<class 'app.Client'>) client_fixture: Client instance.
    """
    queue = Queue()

    server_thread = Thread(
        target=put_func_return_into_queue,
        args=(queue, run_server, '0.0.0.0', 8080)
    )
    server_thread.start()

    client_fixture.run()

    server_thread.join()
    response_from_server = queue.get()

    assert 'status' in response_from_server, f'Invalid response: {response_from_server}'
