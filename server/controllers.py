"""Controllers for server side of Messenger app."""
import base64
import hmac
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from db.models import Client, Message, ClientSession, ClientContact
from db.database import session_scope

from db.settings import SECRET_KEY
from db.utils import (
    login, authenticate, get_validation_errors,
    add_client_to_active_list, remove_from_active_clients
)
from decorators import login_required
from protocol import make_response
from utils import get_socket_info


def register_controller(request):
    errors = get_validation_errors(request, 'login', 'password')
    if errors:
        return make_response(request, 400, {'errors': errors})

    data = request.get('data')
    client_login = data.get('login')

    hmac_obj = hmac.new(
        SECRET_KEY.encode(), data.get('password').encode(), digestmod='sha256'
    )
    password_digest = hmac_obj.hexdigest()

    bytes_photo = base64.decodebytes(bytes(data.get('photo'), 'UTF-8'))

    client = Client(
        name=client_login, password=password_digest, photo=bytes_photo
    )

    try:
        with session_scope() as session:
            session.add(client)

        token = login(request, client)
        add_client_to_active_list(request, client)
        return make_response(request, 200, {'token': token})

    except IntegrityError:
        data = {'errors': f'Client with name {client_login} already exists.'}
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
            add_client_to_active_list(request, client)
            return make_response(request, 200, {'token': token})
        else:
            data = {'errors': 'Enter correct login or password.'}
            return make_response(request, 400, data)

    except ValueError:
        data = {'errors': 'Client already logged in.'}
        return make_response(request, 403, data)


@login_required
def logout_controller(request):
    with session_scope(expire=False) as session:
        client_session = session.query(ClientSession).filter_by(token=request.get('token')).first()
        if client_session:
            client_session.closed = datetime.now()
            data = 'Client session closed.'
            code = 200
        else:
            data = {'errors': 'Client session not found.'}
            code = 404

    if client_session:
        addr, port = client_session.remote_addr, client_session.remote_port
        remove_from_active_clients(addr, port)

    return make_response(request, code, data)


def presence_controller(request):
    client_name = request.get('data').get('client')
    is_active_session = False

    with session_scope() as session:
        client = session.query(Client).filter_by(name=client_name).first()
        if client:
            active_session = client.sessions.filter_by(closed=None).first()

            if active_session:
                # TODO: Вместо проверки IP сделать проверку MAC, внести изменения в протокол
                last_addr = active_session.remote_addr
                current_addr = request.get('address').get('remote').get('addr')

                if last_addr == current_addr:
                    active_session.closed = datetime.now()
                    is_active_session = True

    token = None
    if is_active_session:
        token = login(request, client)
        add_client_to_active_list(request, client)

    return make_response(request, 200, {'token': token})


def message_controller(request):
    errors = get_validation_errors(request, 'text', 'to_client')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    to_client = request_data.get('to_client')
    text = request_data.get('text')

    with session_scope() as session:
        try:
            to_client = session.query(Client).filter_by(name=to_client).first()

        except AttributeError:
            data = f'Client "{to_client}" not found.'
            return make_response(request, 404, data)

        else:
            from_client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
            from_client_id = from_client.id

            to_client_id = to_client.id

            message = Message(
                text=text, from_client_id=from_client_id,
                to_client_id=to_client_id, created=datetime.fromtimestamp(request.get('time'))
            )
            session.add(message)

            data = {
                'text': text, 'to_client': to_client.name,
                'from_client': from_client.name, 'time': request.get('time')
            }

            to_client_session = to_client.sessions.filter_by(closed=None).first()

            if to_client_session:
                addr, port = to_client_session.remote_addr, to_client_session.remote_port
                r_addr = get_socket_info(addr, port)

                return make_response(request, 200, data, r_addr)

            return make_response(request, 200, data)


def get_messages_controller(request):
    errors = get_validation_errors(request, 'from_date')
    if errors:
        return make_response(request, 400, {'errors': errors})

    data = request.get('data')
    from_date = datetime.fromtimestamp(data.get('from_date'))

    with session_scope() as session:
        try:
            client = session.query(ClientSession).filter_by(token=request.get('token')).first().client

        except AttributeError:
            data = 'Client not found.'
            return make_response(request, 404, data)

        else:
            filtered_gotten_messages = client.gotten_messages.filter(Message.created > from_date).all()

            messages = [
                {
                    'text': msg.text, 'from_client': msg.from_client.name,
                    'to_client': msg.to_client.name, 'created': msg.created.timestamp()
                }
                for msg in filtered_gotten_messages
            ]

            data = {'messages': messages}
            return make_response(request, 200, data)


def upd_message_controller(request):
    errors = get_validation_errors(request, 'message_id', 'new_text')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    message_id = request_data.get('message_id')
    new_text = request_data.get('new_text')

    with session_scope() as session:
        messages = session.query(ClientSession).filter_by(token=request.get('token')).first().client.sent_messages
        message = messages.filter_by(id=message_id).first()

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
        message = messages.filter_by(id=message_id).first()

        if message:
            session.delete(message)
            data = {'message_id': message_id}
            return make_response(request, 200, data)

        else:
            data = f'Message with id #{message_id} not found.'
            return make_response(request, 404, data)


def add_contact_controller(request):
    errors = get_validation_errors(request, 'friend_name')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    friend_name = request_data.get('friend_name')

    with session_scope() as session:
        client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
        friend = session.query(Client).filter_by(name=friend_name).first()

        if client and friend:
            if client.name == friend_name:
                data = 'You can\'t add yourself in your own friend list.'
                return make_response(request, 400, data)

            existing_friend = client.friends.filter_by(friend_id=friend.id).first()
            if existing_friend:
                data = f'{friend.name} already in friend list.'
                return make_response(request, 400, data)

            contact = ClientContact(owner_id=client.id, friend_id=friend.id)
            session.add(contact)

            data = {'friend_id': friend.id, 'friend_name': friend.name}
            return make_response(request, 200, data)

        else:
            data = 'Client not found.'
            return make_response(request, 404, data)


def get_contacts_controller(request):   # TODO: реализован на клиенте, удалить
    with session_scope() as session:
        contacts = session.query(ClientSession).filter_by(token=request.get('token')).first().client.friends.all()

        data = {'contacts': contacts}
        return make_response(request, 200, data)


def del_contact_controller(request):
    errors = get_validation_errors(request, 'friend')
    if errors:
        return make_response(request, 400, {'errors': errors})

    request_data = request.get('data')
    friend_name = request_data.get('friend')

    with session_scope() as session:
        client = session.query(ClientSession).filter_by(token=request.get('token')).first().client
        friend_list = client.friends.all()

        for friend in friend_list:
            if friend.friend_contact.name == friend_name:
                session.delete(friend)

                data = {'deleted_friend': friend_name}
                return make_response(request, 200, data)

        data = f'Client "{friend_name}" not found in "{client.name}" friend list.'
        return make_response(request, 404, data)
