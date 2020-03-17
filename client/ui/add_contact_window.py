from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit


class AddContactWindow(QDialog):
    add_contact_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setFixedSize(350, 120)
        self.setWindowTitle('Add new contact')
        self.setModal(True)

        self.label = QLabel('Enter username:', self)
        self.label.setFixedSize(200, 20)
        self.label.move(10, 0)

        self.contact_name = QLineEdit(self)
        self.contact_name.setFixedSize(200, 20)
        self.contact_name.move(10, 30)

        self.add_btn = QPushButton('Add', self)
        self.add_btn.setFixedSize(100, 30)
        self.add_btn.move(230, 20)
        self.add_btn.clicked.connect(self.add_btn_handler)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedSize(100, 30)
        self.cancel_btn.move(230, 60)
        self.cancel_btn.clicked.connect(self.close)

    def add_btn_handler(self):
        contact = self.contact_name.text()
        self.add_contact_signal.emit(contact)
