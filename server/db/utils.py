import hashlib
import hmac
from collections import namedtuple
from datetime import datetime

from sqlalchemy import and_

from db.database import session_scope
from db.models import ClientSession, Client, ActiveClient
from db.settings import SECRET_KEY


def get_validation_errors(request, *attrs):
    """Get errors if some attributes not in request."""
    data = request.get('data')
    message = 'Attribute is required'
    return {attr: message for attr in attrs if attr not in data}


def authenticate(login, password):
    """Authenticate client based on valid login and password."""
    with session_scope() as session:
        client = session.query(Client).filter_by(name=login).first()
        hmac_obj = hmac.new(SECRET_KEY.encode(), password.encode())
        password_digest = hmac_obj.hexdigest()

        if client and hmac.compare_digest(password_digest, client.password.encode()):
            active_session = client.sessions.filter_by(closed=None).first()
            if active_session:
                raise ValueError
            return client


def login(request, client):
    """Make client session (logging in) and get token for client."""
    with session_scope(expire=False) as session:
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


def get_connections():
    with session_scope(expire=False) as session:
        return session.query(ActiveClient).all()


def get_client_stats():
    # TODO: Разобраться с lazy загрузкой при relationship.
    #  Связанные объекты не передаются за пределы сессии.
    #  По итогу надо переработать этот костыль, чтобы при передаче
    #  объекта clients за пределы сессии были доступны все связанные объекты
    with session_scope(expire=False) as session:
        clients = session.query(Client).all()

        Client_stats = namedtuple('Client_stats', [
            'client_id', 'client_name', 'last_login', 'sent_messages_qty', 'gotten_messages_qty'
        ])

        stats_list = list()

        for client in clients:
            client_id = str(client.id)
            client_name = client.name
            last_login = str(
                client.sessions.order_by(ClientSession.created.desc()).first().created.replace(microsecond=0)
            )
            sent_messages_qty = str(client.sent_messages.count())
            gotten_messages_qty = str(client.gotten_messages.count())

            stats = Client_stats(client_id, client_name, last_login, sent_messages_qty, gotten_messages_qty)
            stats_list.append(stats)

        return stats_list


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
        active_client = session.query(ActiveClient).filter(
            and_(ActiveClient.addr == addr, ActiveClient.port == port)
        ).first()

        if active_client:
            session.delete(active_client)


def clear_active_clients_list():
    with session_scope() as session:
        active_connections = session.query(ActiveClient).all()

        for connection in active_connections:
            session.delete(connection)
