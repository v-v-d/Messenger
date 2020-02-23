import hashlib

from db.database import session_scope
from db.models import ClientSession, Client
from db.settings import SECRET_KEY


def get_validation_errors(request, *attrs):
    data = request.get('data')
    errs = {}
    [errs.update({attr: 'Attribute is required!'}) for attr in attrs if attr not in data]
    return errs


def get_message(request, messages):
    request_data = request.get('data')
    message_id = request_data.get('message_id')
    for msg in messages:    # TODO: Оптимизировать поиск
        if msg.id == message_id:
            return msg


def authenticate(login, password):
    with session_scope() as session:
        client = session.query(Client).filter_by(name=login).first()

        if client and password == client.password:
            for client_session in client.sessions:
                if not client_session.closed:
                    raise ValueError
            return client


def login(request, client):
    with session_scope() as session:
        hash_obj = hashlib.sha256()
        hash_obj.update(SECRET_KEY.encode('UTF-8'))
        hash_obj.update(str(request.get('time')).encode('UTF-8'))
        token = hash_obj.hexdigest()

        socket_info = request.get('address')
        remote_socket_info = socket_info.get('remote')
        local_socket_info = socket_info.get('local')

        client_session = ClientSession(
            client=client,
            token=token,
            remote_addr=remote_socket_info.get('addr'),
            remote_port=remote_socket_info.get('port'),
            local_addr=local_socket_info.get('addr'),
            local_port=local_socket_info.get('port')
        )
        session.add(client_session)
        return token
