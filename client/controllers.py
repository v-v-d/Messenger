from datetime import datetime

from db.database import session_scope
from db.models import ClientSession, Message, ClientContact


def add_session_controller(response):
    if response.get('code') == 200:
        data = response.get('data')
        token = data.get('token')

        if token:
            socket_info = response.get('address')
            remote_socket_info = socket_info.get('remote')
            local_socket_info = socket_info.get('local')

            with session_scope() as session:
                last_session = session.query(ClientSession).order_by(ClientSession.id.desc()).first()
                if last_session:
                    last_session.closed = datetime.now()

                client_session = ClientSession(
                    token=token,
                    remote_addr=remote_socket_info.get('addr'),
                    remote_port=remote_socket_info.get('port'),
                    local_addr=local_socket_info.get('addr'),
                    local_port=local_socket_info.get('port')
                )
                session.add(client_session)

                return token


def close_session_controller(response):
    if response.get('code') == 200:
        with session_scope() as session:
            last_session = session.query(ClientSession).order_by(ClientSession.id.desc()).first()
            if last_session and not last_session.closed:
                last_session.closed = datetime.now()


def message_controller(response):
    if response.get('code') == 200:
        data = response.get('data')
        text = data.get('text')
        created = datetime.fromtimestamp(data.get('time'))
        from_client = data.get('from_client')
        to_client = data.get('to_client')

        with session_scope() as session:
            message = Message(
                text=text, from_client=from_client,
                to_client=to_client, created=created
            )

            session.add(message)


def upd_message_controller(response):
    if response.get('code') == 200:
        data = response.get('data')
        message_id = data.get('message_id')
        new_text = data.get('new_text')

        with session_scope() as session:
            message = session.query(Message).filter_by(id=message_id).first()

            if message:
                message.text = new_text
                message.edited = True


def get_messages_controller(response):
    pass


def del_message_controller(response):
    if response.get('code') == 200:
        message_id = response.get('data').get('message_id')

        with session_scope() as session:
            message = session.query(Message).filter_by(id=message_id).first()

            if message:
                session.delete(message)


def add_contact_controller(response):
    if response.get('code') == 200:
        data = response.get('data')
        friend_name = data.get('friend_name')
        friend_id = data.get('friend_id')

        with session_scope() as session:
            contact = ClientContact(friend=friend_name, friend_id=friend_id)
            session.add(contact)


def get_contacts_controller(response):
    pass


def del_contact_controller(response):
    if response.get('code') == 200:
        data = response.get('data')
        friend_id = data.get('friend_id')

        with session_scope() as session:
            contact = session.query(ClientContact).filter_by(friend_id=friend_id).first()

            if contact:
                session.delete(contact)
