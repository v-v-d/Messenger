import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from psutil import process_iter
from signal import SIGTERM


def run_server(server_address, server_port):
    server_socket = socket(AF_INET, SOCK_STREAM)

    try:
        server_socket.bind((server_address, server_port))
        server_socket.listen(5)

        while True:
            client, client_addr = server_socket.accept()

            try:
                request = json.loads(client.recv(1024).decode('UTF-8'))

            except Exception as error:
                print('Recv server error: ', error)

            else:
                if request:
                    print('request: ', request)
                    request.update({'echo': True})
                    client.send(json.dumps(request).encode('UTF-8'))
                    break

    except Exception as error:
        print('Server error: ', error)

    finally:
        server_socket.close()


def run_client(client_address, server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        try:
            client_socket.connect((client_address, server_port))
            request = {'test': 'test'}
            client_socket.send(json.dumps(request).encode('UTF-8'))

        except Exception as error:
            print('Client connection error: ', error)

        else:
            response = json.loads(client_socket.recv(1024).decode('UTF-8'))
            print('response: ', response)

    except Exception as error:
        print('Client error: ', error)

    finally:
        client_socket.close()


def kill_process():
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 8080:
                proc.send_signal(SIGTERM)
                break


if __name__ == '__main__':
    Thread(target=run_server, args=('0.0.0.0', 8080)).start()

    run_client('localhost', 8080)

    kill_process()
