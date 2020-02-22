from datetime import datetime

from sqlalchemy.exc import IntegrityError

from db.models import Client, Message, ClientSession, ClientContact
from db.database import session_scope
from db.utils import get_message, login, authenticate
from protocol import make_response


# TODO: Добавить валидацию реквестов

def register_controller(request):
    data = request.get('data')
    client_login = data.get('login')

    client = Client(name=client_login, password=data.get('password'))

    try:
        with session_scope() as session:
            session.add(client)

        token = login(request, client)
        data = {'text': 'Register done! Now you are logging in.', 'token': token}
        response = make_response(request, 200, data)

    except IntegrityError:
        data = {'text': f'Client with name {client_login} already exists.'}
        response = make_response(request, 400, data)

    return response


def login_controller(request):
    data = request.get('data')

    try:
        client = authenticate(data.get('login'), data.get('password'))

        if client:
            token = login(request, client)
            data = {'text': 'Login done!', 'token': token}
            response = make_response(request, 200, data)
        else:
            data = {'text': 'Enter correct login or password.'}
            response = make_response(request, 400, data)

    except ValueError:
        data = {'text': 'Client already logged in.'}
        response = make_response(request, 403, data)

    return response


def logout_controller(request):
    with session_scope() as session:
        client_session = session.query(ClientSession).filter_by(token=request.get('token')).first()
        if client_session:
            client_session.closed = datetime.now()
            data = {'text': 'Client session closed.'}
            response = make_response(request, 200, data)
        else:
            data = {'text': 'Client session not found.'}
            response = make_response(request, 404, data)

    return response


def presence_controller(request):
    client_name = request.get('data').get('client')
    is_active_session = False

    with session_scope() as session:
        client = session.query(Client).filter_by(name=client_name).first()
        if client:
            for client_session in client.sessions:
                if not client_session.closed:
                    client_session.closed = datetime.now()
                    is_active_session = True

    if is_active_session:
        token = login(request, client)
        response = make_response(request, 200, {'token': token})
    else:
        response = make_response(request, 200, {'token': None})

    return response


def message_controller(request):
    request_data = request.get('data')
    to_client = request_data.get('to_client_id')
    text = request_data.get('text')

    with session_scope() as session:
        try:
            from_client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
            from_client_id = from_client.id

            message = Message(
                text=text, from_client_id=from_client_id,
                to_client_id=to_client, created=datetime.fromtimestamp(request.get('time'))
            )
            session.add(message)

            query = session.query(ClientSession).filter_by(client_id=to_client)
            to_client_session = query.filter_by(closed=None).first()
            addr, port = to_client_session.remote_addr, to_client_session.remote_port

            socket_info = request.get('address')
            remote_socket_info = socket_info.get('remote')
            remote_socket_info['addr'], remote_socket_info['port'] = addr, port

            data = {'text': text, 'from': from_client.name, 'time': request.get('time')}
            response = make_response(request, 200, data)

        except AttributeError:
            data = {'text': f'Client with id #{to_client} not found.'}
            response = make_response(request, 404, data)

    return response


def get_messages_controller(request):
    data = request.get('data')

    with session_scope() as session:
        try:
            messages = session.query(ClientSession).filter_by(token=request.get('token')).first().client.gotten_messages
            filtered_messages = [
                {'id': msg.id, 'text': msg.text, 'from_client': msg.from_client.name, 'date': msg.created.timestamp()}
                for msg in messages
                if msg.created >= datetime.fromtimestamp(float(data.get('from_date')))
            ]
            session.expunge_all()
            data = {'text': 'Success!', 'messages': filtered_messages}
            response = make_response(request, 200, data)

        except AttributeError:
            data = {'text': 'Client not found.'}
            response = make_response(request, 404, data)

    return response


def upd_message_controller(request):
    request_data = request.get('data')
    message_id = request_data.get('message_id')
    new_text = request_data.get('new_text')

    with session_scope() as session:
        messages = session.query(ClientSession).filter_by(token=request.get('token')).first().client.sent_messages
        message = get_message(request, messages)

        if message:
            message.text = new_text
            data = {'text': 'Success updating!', 'new_text': new_text}
            response = make_response(request, 200, data)

        else:
            data = {'text': f'Message with id #{message_id} not found.'}
            response = make_response(request, 404, data)

    return response


def del_message_controller(request):
    request_data = request.get('data')
    message_id = request_data.get('message_id')

    with session_scope() as session:
        messages = session.query(ClientSession).filter_by(token=request.get('token')).first().client.sent_messages
        message = get_message(request, messages)

        if message:
            session.delete(message)
            data = {'text': 'Success deleting!'}
            response = make_response(request, 200, data)

        else:
            data = {'text': f'Message with id #{message_id} not found.'}
            response = make_response(request, 404, data)

    return response


def add_contact_controller(request):
    request_data = request.get('data')
    client_id = request_data.get('client_id')

    with session_scope() as session:
        client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
        friend = session.query(Client).filter_by(id=client_id).first()

        if client and friend:
            contact = ClientContact(owner_id=client.id, friend_id=client_id)
            session.add(contact)

            data = {'text': 'Success contact adding!'}
            response = make_response(request, 200, data)

        else:
            data = {'text': 'Client not found.'}
            response = make_response(request, 404, data)

    return response


def get_contacts_controller(request):
    with session_scope() as session:
        contacts = session.query(ClientSession).filter_by(token=request.get('token')).first().client.friends

        data = {'text': 'Success contacts reading!', 'contacts': contacts}
        return make_response(request, 200, data)


def del_contact_controller(request):
    request_data = request.get('data')
    friend_id = request_data.get('friend_id')

    with session_scope() as session:
        client = session.query(ClientSession).filter_by(token=request.get('token')).first().client

        for friend_contact in client.friends:
            if friend_contact.friend_id == friend_id:
                session.delete(friend_contact)

                data = {'text': 'Success contact deleting!'}
                return make_response(request, 200, data)

        data = {'text': 'Client not found.'}
        return make_response(request, 404, data)