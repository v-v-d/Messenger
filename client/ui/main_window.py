from PyQt5.QtCore import QRect, pyqtSignal, Qt
from PyQt5.QtGui import (
    QStandardItemModel, QStandardItem, QBrush, QColor, QIcon,
    QFont,
    QTextCharFormat)
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTextEdit, QPushButton, QLabel,
    QListView, QMenuBar, QMenu, QStatusBar, QAction, qApp,
    QMessageBox
)


class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()
    send_message_signal = pyqtSignal(str, str)
    start_chatting_signal = pyqtSignal(str)
    switch_to_add_contact = pyqtSignal()
    switch_to_del_contact = pyqtSignal()

    def __init__(self, client_name):
        super().__init__()

        self.setFixedSize(756, 574)
        self.setWindowTitle(f'Python Messenger ({client_name})')

        central_widget = QWidget()

        self.label_contacts = QLabel('Contact list:', central_widget)
        self.label_contacts.setGeometry(QRect(10, 0, 101, 16))

        self.add_contact_btn = QPushButton('Add contact', central_widget)
        self.add_contact_btn.setGeometry(QRect(10, 450, 121, 31))

        self.remove_contact_btn = QPushButton('Remove contact', central_widget)
        self.remove_contact_btn.setGeometry(QRect(140, 450, 121, 31))

        self.label_history = QLabel('Chat room:', central_widget)
        self.label_history.setGeometry(QRect(300, 0, 391, 21))

        self.text_message = QTextEdit(central_widget)
        self.text_message.setGeometry(QRect(300, 360, 441, 71))

        self.label_new_message = QLabel('Enter message here:', central_widget)
        self.label_new_message.setGeometry(QRect(300, 330, 450, 16))

        self.toolbar = self.addToolBar('Formatting')

        self.char_style_resolver = {
            'bold': self.set_text_to_bold,
            'italic': self.set_text_to_italic,
            'underline': self.set_text_to_underline,
        }
        self.font_weight = 50
        self.font_italic = False
        self.font_underline = False

        self.text_font = QFont()

        self.text_bold = QAction(QIcon('client/ui/icons/b.jpg'), 'Bold', self)
        self.text_bold.triggered.connect(lambda: self.set_char_style('bold'))

        self.text_italic = QAction(QIcon('client/ui/icons/i.jpg'), 'Italic', self)
        self.text_italic.triggered.connect(lambda: self.set_char_style('italic'))

        self.text_underline = QAction(QIcon('client/ui/icons/u.jpg'), 'Underline', self)
        self.text_underline.triggered.connect(lambda: self.set_char_style('underline'))

        self.toolbar.addActions([
            self.text_bold, self.text_italic, self.text_underline
        ])

        self.list_contacts = QListView(central_widget)
        self.list_contacts.setGeometry(QRect(10, 20, 251, 411))
        self.contacts_model = QStandardItemModel()
        self.list_contacts.setModel(self.contacts_model)

        self.list_messages = QListView(central_widget)
        self.list_messages.setGeometry(QRect(300, 20, 441, 301))
        self.messages_model = QStandardItemModel()
        self.list_messages.setModel(self.messages_model)
        self.is_list_messages_disable = False

        self.send_btn = QPushButton('Send', central_widget)
        self.send_btn.setGeometry(QRect(610, 450, 131, 31))

        self.clear_btn = QPushButton('Clear', central_widget)
        self.clear_btn.setGeometry(QRect(460, 450, 131, 31))

        self.setCentralWidget(central_widget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 756, 21))

        self.menu = QMenu('File', self.menubar)
        self.menu_2 = QMenu('Contacts', self.menubar)

        self.setMenuBar(self.menubar)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.menu_exit = QAction('Exit', self)
        self.menu_logout = QAction('Logout', self)
        self.menu.addAction(self.menu_exit)
        self.menu.addAction(self.menu_logout)

        self.add_contact_menu = QAction('Add new', self)
        self.del_contact_menu = QAction('Remove some', self)
        self.menu_2.addAction(self.add_contact_menu)
        self.menu_2.addAction(self.del_contact_menu)
        self.menu_2.addSeparator()

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.message = QMessageBox()

        self.menu_exit.triggered.connect(qApp.exit)
        self.menu_logout.triggered.connect(self.menu_logout_handler)
        self.send_btn.clicked.connect(self.send_btn_handler)
        self.add_contact_btn.clicked.connect(self.add_contact_btn_handler)
        self.add_contact_menu.triggered.connect(self.add_contact_btn_handler)
        self.remove_contact_btn.clicked.connect(self.del_contact_btn_handler)
        self.del_contact_menu.triggered.connect(self.del_contact_btn_handler)
        self.list_contacts.doubleClicked.connect(self.list_contacts_click_handler)

    def set_elements_disable_status(self, status):
        if not isinstance(status, bool):
            raise ValueError(f'Disable status must be bool. Got {type(status)}')

        self.send_btn.setDisabled(status)
        self.clear_btn.setDisabled(status)
        self.text_message.setDisabled(status)
        self.is_list_messages_disable = status

    def render_welcome_message(self):
        self.messages_model.clear()
        msg = QStandardItem(f'Doubleclick to contact in contact list for start chatting.')
        msg.setEditable(False)
        self.messages_model.appendRow(msg)

    def render_contacts(self, contacts):
        self.contacts_model.clear()

        if contacts and isinstance(contacts, list):
            for contact in contacts:
                rendered_contact = QStandardItem(contact.friend)
                rendered_contact.setEditable(False)
                self.contacts_model.appendRow(rendered_contact)

    def render_messages(self, friend, client_name, messages):
        self.messages_model.clear()

        if messages and isinstance(messages, list):
            for message in messages:
                self.render_message(friend, client_name, message)

            self.list_messages.scrollToBottom()

    def render_message(self, friend, client_name, message):
        if not self.is_list_messages_disable:
            if message.from_client in (friend, client_name):
                date = message.created.replace(microsecond=0)
                text = message.text
                from_client = message.from_client

                msg = QStandardItem(f'{date}\n{from_client}:\n{text}')
                msg.setEditable(False)

                if from_client == client_name:
                    msg.setTextAlignment(Qt.AlignRight)
                    msg.setBackground(QBrush(QColor(240, 240, 240)))

                self.messages_model.appendRow(msg)
                self.list_messages.scrollToBottom()

    def menu_logout_handler(self):
        self.logout_signal.emit()

    def send_btn_handler(self):
        message = self.text_message.toPlainText()
        to_client_name = self.list_contacts.currentIndex().data()
        if message and to_client_name:
            self.send_message_signal.emit(to_client_name, message)
            self.text_message.clear()

    def add_contact_btn_handler(self):
        self.switch_to_add_contact.emit()

    def del_contact_btn_handler(self):
        self.switch_to_del_contact.emit()

    def list_contacts_click_handler(self):
        self.messages_model.clear()
        self.set_elements_disable_status(False)
        friend = self.list_contacts.currentIndex().data()
        self.start_chatting_signal.emit(friend)

    def set_char_style(self, style):
        cursor = self.text_message.textCursor()
        char_format = QTextCharFormat()
        self.char_style_resolver[style](char_format)
        cursor.mergeCharFormat(char_format)

    def set_text_to_bold(self, char_format):
        bold_weight = 600
        thin_weight = 50

        weight = bold_weight if self.font_weight < bold_weight else thin_weight
        char_format.setFontWeight(weight)
        self.font_weight = weight

    def set_text_to_italic(self, char_format):
        char_format.setFontItalic(not self.font_italic)
        self.font_italic = not self.font_italic

    def set_text_to_underline(self, char_format):
        char_format.setFontUnderline(not self.font_underline)
        self.font_underline = not self.font_underline
