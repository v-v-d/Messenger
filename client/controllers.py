"""Controllers for client side of Messenger app."""
from datetime import datetime

from ui.signals import SIGNAL


def add_session_controller(response, database):
    code = response.get('code')
    data = response.get('data')
    if code == 200:
        token = data.get('token')

        if token and database:
            socket_info = response.get('address')
            remote_socket_info = socket_info.get('remote')
            local_socket_info = socket_info.get('local')

            with database.session_scope() as session:
                last_session = (
                    session.query(database.ClientSession)
                    .order_by(database.ClientSession.id.desc())
                    .first()
                )

                if last_session:
                    last_session.closed = datetime.now()

                client_session = database.ClientSession(
                    token=token,
                    remote_addr=remote_socket_info.get('addr'),
                    remote_port=remote_socket_info.get('port'),
                    local_addr=local_socket_info.get('addr'),
                    local_port=local_socket_info.get('port'),
                )
                session.add(client_session)

    if response.get('action') in ('login', 'register'):
        SIGNAL.auth_signal.emit(code, data)

    return data


def close_session_controller(response, database):
    if response.get('code') == 200 and database:
        with database.session_scope() as session:
            last_session = (
                session.query(database.ClientSession)
                .order_by(database.ClientSession.id.desc())
                .first()
            )

            if last_session and not last_session.closed:
                last_session.closed = datetime.now()


def load_messages_to_db_controller(response, database):
    if response.get('code') == 200 and database:
        data = response.get('data')
        messages = data.get('messages')

        if messages:
            sorted(messages, key=lambda msg: msg.get('created'))

            from_date = datetime.fromtimestamp(messages[0].get('created'))

            with database.session_scope(expire=False) as session:
                existing_messages = (
                    session.query(database.Message)
                    .filter(database.Message.created >= from_date)
                    .all()
                )

            existing_messages_dict_list = list()
            if existing_messages:
                existing_messages_dict_list = [
                        {
                            'text': msg.text, 'from_client': msg.from_client,
                            'to_client': msg.to_client, 'created': msg.created
                        }
                        for msg in existing_messages
                    ]

            with database.session_scope() as session:
                for msg in messages:
                    if msg not in existing_messages_dict_list:
                        created = datetime.fromtimestamp(msg.get('created'))
                        message = database.Message(
                            text=msg.get('text'), from_client=msg.get('from_client'),
                            to_client=msg.get('to_client'), created=created
                        )

                        session.add(message)


def message_controller(response, database):
    if response.get('code') == 200 and database:
        data = response.get('data')
        text = data.get('text')
        created = datetime.fromtimestamp(data.get('time'))
        from_client = data.get('from_client')
        to_client = data.get('to_client')

        is_message_exists = False

        with database.session_scope() as session:
            similar_message = (
                session.query(database.Message)
                .filter(
                    database.Message.text == text,
                    database.Message.from_client == from_client,
                    database.Message.to_client == to_client,
                    database.Message.created >= created,
                )
                .first()
            )

            if similar_message:
                is_message_exists = True

        if not is_message_exists:
            with database.session_scope(expire=False) as session:
                message = database.Message(
                    text=text, from_client=from_client,
                    to_client=to_client, created=created
                )

                session.add(message)

                SIGNAL.new_message.emit(from_client, to_client, message)


def upd_message_controller(response, database):
    if response.get('code') == 200 and database:
        data = response.get('data')
        message_id = data.get('message_id')
        new_text = data.get('new_text')

        with database.session_scope() as session:
            message = (
                session.query(database.Message)
                .filter_by(id=message_id)
                .first()
            )

            if message:
                message.text = new_text
                message.edited = True


def del_message_controller(response, database):
    if response.get('code') == 200 and database:
        message_id = response.get('data').get('message_id')

        with database.session_scope() as session:
            message = (
                session.query(database.Message)
                .filter_by(id=message_id)
                .first()
            )

            if message:
                session.delete(message)


def add_contact_controller(response, database):
    if response.get('code') == 200 and database:
        data = response.get('data')
        friend_name = data.get('friend_name')
        friend_id = data.get('friend_id')

        with database.session_scope() as session:
            contact = database.ClientContact(friend=friend_name, friend_id=friend_id)
            session.add(contact)


def del_contact_controller(response, database):
    if response.get('code') == 200 and database:
        data = response.get('data')
        friend = data.get('deleted_friend')

        with database.session_scope() as session:
            contact = (
                session.query(database.ClientContact)
                .filter_by(friend=friend)
                .first()
            )

            if contact:
                session.delete(contact)
