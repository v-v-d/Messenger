from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox


class SignupWindow(QDialog):
    back_to_login_signal = pyqtSignal()
    signup_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.message = QMessageBox()

        self.setWindowTitle('SignUp')
        self.setFixedSize(400, 220)

        self.label_login = QLabel('Login:', self)
        self.label_login.move(30, 10)
        self.label_login.setFixedSize(340, 15)

        self.login = QLineEdit(self)
        self.login.setFixedSize(340, 20)
        self.login.move(30, 30)

        self.label_password_1 = QLabel('Password:', self)
        self.label_password_1.move(30, 60)
        self.label_password_1.setFixedSize(340, 15)

        self.password_1 = QLineEdit(self)
        self.password_1.setFixedSize(340, 20)
        self.password_1.move(30, 80)

        self.label_password_2 = QLabel('Confirm password:', self)
        self.label_password_2.move(30, 110)
        self.label_password_2.setFixedSize(340, 15)

        self.password_2 = QLineEdit(self)
        self.password_2.setFixedSize(340, 20)
        self.password_2.move(30, 130)

        self.back_to_login_btn = QPushButton('< Back', self)
        self.back_to_login_btn.move(30, 170)
        self.back_to_login_btn.clicked.connect(self.back_to_login_btn_handler)

        self.signup_btn = QPushButton('SignUp', self)
        self.signup_btn.move(180, 170)
        self.signup_btn.clicked.connect(self.signup_btn_handler)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.move(280, 170)
        self.cancel_btn.clicked.connect(self.back_to_login_btn_handler)

    def signup_btn_handler(self):
        login = self.login.text()
        password_1 = self.password_1.text()
        password_2 = self.password_2.text()

        if not all((login, password_1, password_2)):
            self.message.warning(self, 'Error', 'Login and password is required.')
        elif all((login, password_1, password_2)) and not password_1 == password_2:
            self.message.warning(self, 'Error', 'Passwords must match.')
        else:
            self.signup_signal.emit(login, password_1)

    def back_to_login_btn_handler(self):
        self.back_to_login_signal.emit()
