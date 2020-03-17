from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, qApp, QMessageBox


class LoginWindow(QDialog):
    switch_to_signup = pyqtSignal()
    login_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.message = QMessageBox()

        self.setWindowTitle('Login')
        self.setFixedSize(400, 170)

        self.label_login = QLabel('Login:', self)
        self.label_login.move(30, 10)
        self.label_login.setFixedSize(340, 15)

        self.login = QLineEdit(self)
        self.login.setFixedSize(340, 20)
        self.login.move(30, 30)

        self.label_password = QLabel('Password:', self)
        self.label_password.move(30, 60)
        self.label_password.setFixedSize(340, 15)

        self.password = QLineEdit(self)
        self.password.setFixedSize(340, 20)
        self.password.move(30, 80)

        self.signup_btn = QPushButton('SignUp', self)
        self.signup_btn.move(30, 120)
        self.signup_btn.clicked.connect(self.signup_btn_handler)

        self.login_btn = QPushButton('Login', self)
        self.login_btn.move(180, 120)
        self.login_btn.clicked.connect(self.login_btn_handler)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.move(280, 120)
        self.cancel_btn.clicked.connect(qApp.exit)

    def login_btn_handler(self):
        login = self.login.text()
        password = self.password.text()
        if not all((login, password)):
            self.message.warning(self, 'Error', 'Login and password is required.')
        else:
            self.login_signal.emit(login, password)

    def signup_btn_handler(self):
        self.switch_to_signup.emit()
