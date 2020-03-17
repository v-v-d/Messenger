"""Controllers for handling local requests."""
import json
from datetime import datetime

from sqlalchemy import or_


def local_message_controller(request, database):
    if database:
        request = set_request_data_to_dict(request)

        created = datetime.fromtimestamp(request.get('time'))
        data = request.get('data')
        text = data.get('text')
        from_client = data.get('from_client')
        to_client = data.get('to_client')

        with database.session_scope(expire=False) as session:
            message = database.Message(
                text=text, from_client=from_client,
                to_client=to_client, created=created
            )

            session.add(message)

            return message


def get_messages_controller(request, database):
    if database:
        request = set_request_data_to_dict(request)
        data = request.get('data')
        from_client = data.get('from_client')
        to_client = data.get('to_client')
        get_last = data.get('get_last')

        with database.session_scope(expire=False) as session:
            messages = (
                session.query(database.Message)
                .filter(
                    or_(database.Message.from_client == from_client, database.Message.from_client == to_client),
                    or_(database.Message.to_client == to_client, database.Message.to_client == from_client),
                )
                .limit(get_last)
                .all()
            )
            return messages if messages else 'None'


def get_contacts_controller(request, database):
    if database:
        with database.session_scope(expire=False) as session:
            contacts = session.query(database.ClientContact).all()

            return contacts if contacts else 'None'


def set_request_data_to_dict(request):
    if request.get('data'):
        request = request.copy()
        request['data'] = json.loads(request.get('data'))
        return request
