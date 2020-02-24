from datetime import datetime

from sqlalchemy.exc import IntegrityError

from db.models import Client, Message, ClientSession, ClientContact
from db.database import session_scope
from db.utils import get_message, login, authenticate, get_validation_errors
from protocol import make_response
from utils import get_socket_info


def register_controller(request):
    errors = get_validation_errors(request, 'login', 'password')
    if errors:
        return make_response(request, 400, {'errors': errors})

    data = request.get('data')
    client_login = data.get('login')

    client = Client(name=client_login, password=data.get('password'))

    try:
        with session_scope() as session:
            session.add(client)

        token = login(request, client)
        return make_response(request, 200, {'token': token})

    except IntegrityError:
        data = f'Client with name {client_login} already exists.'
        return make_response(request, 400, data)


def login_controller(request):
    errors = get_validation_errors(request, 'login', 'password')
    if errors:
        return make_response(request, 400, {'errors': errors})

    data = request.get('data')

    try:
        client = authenticate(data.get('login'), data.get('password'))

        if client:
            token = login(request, client)
            return make_response(request, 200, {'token': token})
        else:
            data = 'Enter correct login or password.'
            return make_response(request, 400, data)

    except ValueError:
        data = 'Client already logged in.'
        return make_response(request, 403, data)


def logout_controller(request):
    with session_scope() as session:
        client_session = session.query(ClientSession).filter_by(token=request.get('token')).first()
        if client_session:
            client_session.closed = datetime.now()
            data = 'Client session closed.'
            return make_response(request, 200, data)
        else:
            data = 'Client session not found.'
            return make_response(request, 404, data)


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

    token = None
    if is_active_session:
        token = login(request, client)
    return make_response(request, 200, {'token': token})


def message_controller(request):
    errors = get_validation_errors(request, 'text', 'to_client_id')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    to_client_id = request_data.get('to_client_id')
    text = request_data.get('text')

    with session_scope() as session:
        try:
            from_client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
            from_client_id = from_client.id

            query = session.query(ClientSession).filter_by(client_id=to_client_id)
            to_client_session = query.filter_by(closed=None).first()

            addr, port = to_client_session.remote_addr, to_client_session.remote_port
            r_addr = get_socket_info(addr, port)

            message = Message(
                text=text, from_client_id=from_client_id,
                to_client_id=to_client_id, created=datetime.fromtimestamp(request.get('time'))
            )
            session.add(message)

            data = {
                'text': text, 'to_client': to_client_session.client.name,
                'from_client': from_client.name, 'time': request.get('time')
            }
            return make_response(request, 200, data, r_addr)

        except AttributeError:
            data = f'Client with id #{to_client_id} not found.'
            return make_response(request, 404, data)


def get_messages_controller(request):
    errors = get_validation_errors(request, 'from_date')
    if errors:
        return make_response(request, 400, {'errors': errors})

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
            data = {'messages': filtered_messages}
            return make_response(request, 200, data)

        except AttributeError:
            data = 'Client not found.'
            return make_response(request, 404, data)


def upd_message_controller(request):
    errors = get_validation_errors(request, 'message_id', 'new_text')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    message_id = request_data.get('message_id')
    new_text = request_data.get('new_text')

    with session_scope() as session:
        messages = session.query(ClientSession).filter_by(token=request.get('token')).first().client.sent_messages
        message = get_message(request, messages)

        if message:
            message.text = new_text
            message.edited = True
            data = {'message_id': message_id, 'new_text': new_text}
            return make_response(request, 200, data)

        else:
            data = f'Message with id #{message_id} not found.'
            return make_response(request, 404, data)


def del_message_controller(request):
    errors = get_validation_errors(request, 'message_id')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    message_id = request_data.get('message_id')

    with session_scope() as session:
        messages = session.query(ClientSession).filter_by(token=request.get('token')).first().client.sent_messages
        message = get_message(request, messages)

        if message:
            session.delete(message)
            data = {'message_id': message_id}
            return make_response(request, 200, data)

        else:
            data = f'Message with id #{message_id} not found.'
            return make_response(request, 404, data)


def add_contact_controller(request):
    errors = get_validation_errors(request, 'friend_id')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    friend_id = request_data.get('friend_id')

    with session_scope() as session:
        client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
        friend = session.query(Client).filter_by(id=friend_id).first()

        if client and friend:
            if client.id == friend_id:
                data = 'You can\'t add yourself in your own friend list.'
                return make_response(request, 400, data)

            for existing_contact in client.friends:
                if existing_contact.friend_contact == friend:
                    data = f'{friend.name} already in friend list.'
                    return make_response(request, 400, data)

            contact = ClientContact(owner_id=client.id, friend_id=friend_id)
            session.add(contact)

            data = {'friend_id': friend_id, 'friend_name': friend.name}
            return make_response(request, 200, data)

        else:
            data = 'Client not found.'
            return make_response(request, 404, data)


def get_contacts_controller(request):
    with session_scope() as session:
        contacts = session.query(ClientSession).filter_by(token=request.get('token')).first().client.friends

        data = {'contacts': contacts}
        return make_response(request, 200, data)


def del_contact_controller(request):
    errors = get_validation_errors(request, 'friend_id')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    friend_id = request_data.get('friend_id')

    with session_scope() as session:
        client = session.query(ClientSession).filter_by(token=request.get('token')).first().client

        for friend_contact in client.friends:
            if friend_contact.friend_id == friend_id:
                session.delete(friend_contact)

                data = {'friend_id': friend_id}
                return make_response(request, 200, data)

        data = 'Client not found in friend list.'
        return make_response(request, 404, data)
