"""Controllers for handling local requests."""
import json
from datetime import datetime

from db.database import session_scope
from db.models import Message, ClientContact


def get_messages_controller(request):
    set_request_data_to_dict(request)
    timestamp = request.get('data').get('from_date')
    date = datetime.fromtimestamp(timestamp)
    with session_scope() as session:
        messages = session.query(Message).filter(Message.created >= date).all()
        print(messages)
        return messages


def get_contacts_controller(request):
    with session_scope() as session:
        contacts = session.query(ClientContact).all()
        print(contacts)
        return contacts


def set_request_data_to_dict(request):
    if request.get('data'):
        request['data'] = json.loads(request.get('data'))  # TODO: Убрать после появления GUI
