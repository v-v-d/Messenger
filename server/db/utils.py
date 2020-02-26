import hashlib
from datetime import datetime

from sqlalchemy import and_

from db.database import session_scope, no_expire_session_scope
from db.models import ClientSession, Client, ActiveClient
from db.settings import SECRET_KEY


def get_validation_errors(request, *attrs):
    data = request.get('data')
    errs = {}
    [errs.update({attr: 'Attribute is required!'}) for attr in attrs if attr not in data]
    return errs


def authenticate(login, password):
    with session_scope() as session:
        client = session.query(Client).filter_by(name=login).first()

        if client and password == client.password:
            active_session = client.sessions.filter_by(closed=None).first()
            if active_session:
                raise ValueError
            return client


def login(request, client):
    with no_expire_session_scope() as session:
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


def get_active_sessions():
    with session_scope() as session:
        return session.query(ClientSession).filter_by(closed=None).all()


def get_clients():
    with session_scope() as session:
        return session.query(Client).all()


def add_client_to_active_list(request, client):
    client_address = request.get('address').get('remote')
    addr = client_address.get('addr')
    port = client_address.get('port')
    created = datetime.fromtimestamp(request.get('time'))

    with session_scope() as session:
        if client:
            active_client = ActiveClient(
                client_id=client.id,
                client_name=client.name,
                addr=addr, port=port,
                created=created
            )
            session.add(active_client)


def remove_from_active_clients(addr, port):
    with session_scope() as session:
        active_connection = session.query(ActiveClient).filter(
            and_(ActiveClient.addr == addr, ActiveClient.port == port)
        ).first()

        if active_connection:
            session.delete(active_connection)
