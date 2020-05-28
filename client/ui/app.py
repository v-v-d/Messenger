import sys
from logging import getLogger
from logging.config import dictConfig
from time import sleep

from PyQt5.QtWidgets import QApplication, qApp

from db.local_storage import LocalStorage
from db.utils import (
    set_client_last_visit_date, set_client_to_inactive,
    add_client_to_clients_db, get_client_last_visit_date,
    set_client_to_active
)
from log.log_config import LOGGING
from ui.add_contact_window import AddContactWindow
from ui.del_contact_window import DelContactWindow
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.signals import SIGNAL
from ui.signup_window import SignupWindow


class GUIApplication:
    def __init__(self, client):
        self.client = client
        self.login_window = None
        self.signup_window = None
        self.main_window = None
        self.add_contact_window = None
        self.del_contact_window = None
        self.client_name = None
        self.current_friend = None

        dictConfig(LOGGING)
        self.logger = getLogger('client')

    def __enter__(self):
        self.make_signals_connection()
        self.logger.info('Client GUI was rendered.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client.client_name:
            set_client_last_visit_date(self.client.client_name)
        if exc_type and not exc_type == SystemExit and exc_val:
            self.logger.critical(
                f'Client GUI closed with error: {exc_type}: {exc_val}.'
            )
        else:
            self.logger.info('Client GUI closed.')
        return True

    def render(self):
        app = QApplication(sys.argv)

        self.set_up_login_window()
        self.set_up_signup_window()
        self.set_up_add_contact_window()
        self.set_up_del_contact_window()

        if self.client.client_name:
            max_waiting_time = 0
            while True:  # TODO: переделать этот костыль
                if self.client.token:
                    last_visit_date = get_client_last_visit_date(self.client.client_name)
                    set_client_to_active(self.client.client_name)
                    self.get_new_messages_from_server(last_visit_date)
                    break

                sleep(0.5)
                max_waiting_time += 0.5

                if max_waiting_time == 10:
                    self.main_window.message.critical(
                        self.main_window, 'Error', 'Server timed out.'
                    )
                    qApp.exit()

            self.show_main_window()
        else:
            self.show_login_window()

        sys.exit(app.exec_())

    def set_up_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.login_signal.connect(self.login)
        self.login_window.switch_to_signup.connect(self.show_signup_window)

    def set_up_signup_window(self):
        self.signup_window = SignupWindow()
        self.signup_window.signup_signal.connect(self.signup)
        self.signup_window.back_to_login_signal.connect(self.show_login_window)

    def set_up_add_contact_window(self):
        self.add_contact_window = AddContactWindow()
        self.add_contact_window.add_contact_signal.connect(self.add_contact)

    def set_up_del_contact_window(self):
        self.del_contact_window = DelContactWindow()
        self.del_contact_window.del_contact_signal.connect(self.del_contact)

    def show_login_window(self):
        self.login_window.login.clear()
        self.login_window.password.clear()

        if self.signup_window:
            self.signup_window.close()
        if self.main_window:
            self.main_window.close()

        self.login_window.show()

    def show_signup_window(self):
        self.signup_window.login.clear()
        self.signup_window.password_1.clear()
        self.signup_window.password_2.clear()

        if self.login_window:
            self.login_window.close()

        self.signup_window.show()

    def show_main_window(self):
        self.main_window = MainWindow(self.client.client_name)
        self.main_window.logout_signal.connect(self.logout)
        self.main_window.start_chatting_signal.connect(self.start_chatting)
        self.main_window.send_message_signal.connect(self.send_message)
        self.main_window.switch_to_add_contact.connect(self.show_add_contact_window)
        self.main_window.switch_to_del_contact.connect(self.show_del_contact_window)

        self.make_main_window_signals_connection()

        self.main_window.set_elements_disable_status(True)
        self.main_window.render_welcome_message()

        contacts = self.get_contacts()
        self.main_window.render_contacts(contacts)

        if self.login_window:
            self.login_window.close()
        if self.signup_window:
            self.signup_window.close()

        self.main_window.show()

    def show_add_contact_window(self):
        self.add_contact_window.contact_name.clear()
        self.add_contact_window.show()

    def show_del_contact_window(self):
        self.del_contact_window.selector.clear()
        self.del_contact_window.render_del_contacts_list(self.get_contacts())
        self.del_contact_window.show()

    def login(self, login, password):
        self.client_name = login

        action = 'login'
        data = {'login': login, 'password': password}
        self.write(action, data)

    def signup(self, login, password, photo):
        self.client_name = login

        action = 'register'
        data = {'login': login, 'password': password, 'photo': photo}
        self.write(action, data)

    def logout(self):
        action = 'logout'
        self.write(action)

        self.main_window.close()

        self.client.client_name = None
        set_client_to_inactive()

        qApp.exit()     # TODO: Вместо qApp.exit() показать окно логина, удалить connect к текущей db

    def create_account(self, code, data):
        if code == 200:
            add_client_to_clients_db(self.client_name)
            self.set_client_name_and_connect_to_db()

            last_visit_date = get_client_last_visit_date(self.client_name)
            set_client_to_active(self.client_name)

            self.get_new_messages_from_server(last_visit_date)

            self.show_main_window()
        else:
            errors = ', '.join([f'{key}: {val}' for key, val in data.get('errors').items()])
            self.login_window.message.critical(self.login_window, 'Error', errors)

    def set_client_name_and_connect_to_db(self):
        if self.client_name:
            self.client.client_name = self.client_name
            self.client.database = LocalStorage(self.client_name)
            self.client.database.connect()

    def start_chatting(self, friend):
        self.current_friend = friend
        messages = self.get_messages(self.current_friend)
        self.main_window.render_messages(
            self.current_friend, self.client.client_name, messages
        )

    def get_messages(self, friend):
        action = 'get_local_messages'
        data = {
            'from_client': self.client.client_name,
            'to_client': friend,
            'get_last': 20,
        }
        return self.write(action, data)

    def send_message(self, to_client_name, message):
        action = 'message'
        data = {'text': message, 'to_client': to_client_name}
        self.write(action, data)

        local_action = 'local_message'
        local_data = {
            'text': message, 'to_client': to_client_name,
            'from_client': self.client.client_name
        }
        message = self.write(local_action, local_data)

        self.main_window.render_message(
            to_client_name, self.client.client_name, message
        )

    def add_contact(self, contact):
        action = 'add_contact'
        data = {'friend_name': contact}
        self.write(action, data)

    def del_contact(self, contact):
        self.main_window.messages_model.clear()
        action = 'del_contact'
        data = {'friend': contact}
        self.write(action, data)

    def get_contacts(self):
        action = 'get_contacts'
        return self.write(action)

    def get_new_messages_from_server(self, from_date):
        time = from_date.timestamp()
        action = 'get_messages'
        data = {'from_date': time}
        self.write(action, data)

    def write(self, action, data=None):
        try:
            result = self.client.write(action, data)
        except:
            self.main_window.message.critical(
                self.main_window, 'Error', 'Can\'t send data to server.'
            )
        else:
            return result

    def validate_render_message(self, friend, client_name, messages):
        if friend == self.current_friend:
            self.main_window.render_message(friend, client_name, messages)

    def make_signals_connection(self):
        SIGNAL.auth_signal.connect(self.create_account)
        SIGNAL.new_message.connect(self.validate_render_message)

    def make_main_window_signals_connection(self):
        SIGNAL.contact_signal.connect(
            lambda: self.main_window.render_contacts(self.get_contacts())
        )
