from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton


class DelContactWindow(QDialog):
    del_contact_signal = pyqtSignal(str)

    def __init__(self,):
        super().__init__()

        self.setFixedSize(350, 120)
        self.setWindowTitle('Delete contact')
        self.setModal(True)

        self.selector_label = QLabel('Choose contact:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.del_btn = QPushButton('Delete', self)
        self.del_btn.setFixedSize(100, 30)
        self.del_btn.move(230, 20)
        self.del_btn.clicked.connect(self.del_btn_handler)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedSize(100, 30)
        self.cancel_btn.move(230, 60)
        self.cancel_btn.clicked.connect(self.close)

    def render_del_contacts_list(self, contacts):
        if contacts and isinstance(contacts, list):
            for contact in contacts:
                self.selector.addItem(contact.friend)

    def del_btn_handler(self):
        contact = self.selector.currentText()
        self.del_contact_signal.emit(contact)
