"""
Fake DB. Dict with client names as keys and clients socket objects as values:
CLIENTS_DB ={
    'client_name_1': <class 'socket.socket'>,
    'client_name_2': <class 'socket.socket'>,
    ...
}
"""

CLIENTS_DB = {}


def add_client_to_db(request, socket):
    """
    Add client to CLIENTS_DB dict.
    :param (dict) request: Dict with request body.
    :param (<class 'socket.socket'>) socket: Client socket.
    """
    if request.get('action') == 'presence':
        client_name = request.get('user')
        if not is_client_in_db(client_name):
            CLIENTS_DB.update({client_name: socket})


def get_client_from_db(request):
    """
    Get client from DB by client name.
    :param (dict) request: Client request body.
    :return (<class 'socket.socket'>) : Client socket.
    """
    from_client = request.get('user')
    to_client = request.get('data').get('to_user')
    if is_client_in_db(to_client):
        client = CLIENTS_DB.get(to_client)
    else:
        client = CLIENTS_DB.get(from_client)
    return client


def remove_client_from_db(client_socket):
    """
    Remove client from DB.
    :param (<class 'socket.socket'>) client_socket: Client socket.
    """
    if client_socket in CLIENTS_DB.values():
        for key, value in CLIENTS_DB.items():
            if value == client_socket:
                CLIENTS_DB.pop(key)
                break


def is_client_in_db(client_name):
    """
    Check that client in DB.
    :param (str) client_name: Client name.
    :return (bool) : True if client in DB, False otherwise.
    """
    return client_name in CLIENTS_DB
