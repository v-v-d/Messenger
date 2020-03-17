from datetime import datetime

from db.clients_db import session_scope, Client


def add_client_to_clients_db(client_name):
    with session_scope() as session:
        existing_client = session.query(Client).filter_by(name=client_name).first()

        if not existing_client:
            client = Client(
                name=client_name,
                is_active=True
            )
            session.add(client)

    set_client_to_active(client_name)


def get_active_client_from_clients_db():
    with session_scope(expire=False) as session:
        return session.query(Client).filter_by(is_active=True).first()


def set_client_to_active(client_name):
    with session_scope() as session:
        query = session.query(Client)
        clients = query.all()
        current_client = query.filter_by(name=client_name).first()

        for client in clients:
            if client is current_client:
                client.is_active = True
                client.last_visit = datetime.now()


def get_client_last_visit_date(client_name):
    with session_scope() as session:
        client = session.query(Client).filter_by(name=client_name).first()

        if client:
            return client.last_visit


def set_client_last_visit_date(client_name):
    with session_scope() as session:
        client = session.query(Client).filter_by(name=client_name).first()
        client.last_visit = datetime.now()


def get_active_client_name_from_clients_db():
    client = get_active_client_from_clients_db()

    if client:
        return client.name


def set_client_to_inactive():
    with session_scope() as session:
        active_client = session.query(Client).filter_by(is_active=True).first()

        if active_client:
            active_client.is_active = False
