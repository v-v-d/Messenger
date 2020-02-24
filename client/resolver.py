from controllers import *


RESOLVER = {
    'presence': add_session_controller,

    'login': add_session_controller,
    'logout': close_session_controller,
    'register': add_session_controller,

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
