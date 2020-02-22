"""
Resolver for server side of Messenger app. The key is the name
of the action, and the value is the name of the controller that
resolve this action.
"""
from controllers import *


RESOLVER = {
    'presence': presence_controller,

    'login': login_controller,
    'logout': logout_controller,
    'register': register_controller,

    'message': message_controller,
    'get_messages': get_messages_controller,
    'upd_message': upd_message_controller,
    'del_message': del_message_controller,

    'add_contact': add_contact_controller,
    'get_contacts': get_contacts_controller,
    'del_contact': del_contact_controller,
}


def get_controller(action_name):
    """Get controller by action name.
    :param (str) action_name: Action name passed from client.
    :return (<class 'function'>): Controller associated with passed action name.
    """
    return RESOLVER.get(action_name)
