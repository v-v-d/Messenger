"""
Resolvers for client side of Messenger app. The key is the name
of the action, and the value is the name of the controller that
resolve this action.
"""

from controllers import *
from local_controllers import *


RESPONSE_RESOLVER = {
    'presence': add_session_controller,

    'login': add_session_controller,
    'logout': close_session_controller,
    'register': add_session_controller,

    'get_messages': load_messages_to_db_controller,
    'message': message_controller,
    'upd_message': upd_message_controller,
    'del_message': del_message_controller,

    'add_contact': add_contact_controller,
    'del_contact': del_contact_controller,
}


LOCAL_REQUEST_RESOLVER = {
    'local_message': local_message_controller,
    'get_local_messages': get_messages_controller,
    'get_contacts': get_contacts_controller,
}


def get_response_controller(action_name):
    """Get controller by action name.
    :param (str) action_name: Action name passed from client.
    :return (<class 'function'>): Controller associated with passed action name.
    """
    return RESPONSE_RESOLVER.get(action_name)


def get_local_request_controller(action_name):
    """Get local controller by action name.
    :param (str) action_name: Action name passed from client.
    :return (<class 'function'>): Controller associated with passed action name.
    """
    return LOCAL_REQUEST_RESOLVER.get(action_name)
