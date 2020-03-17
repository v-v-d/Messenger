from PyQt5.QtCore import pyqtSignal, QObject

from db.local_storage import LocalStorage


class SenderObject(QObject):
    new_message = pyqtSignal(str, str, LocalStorage.Message)
    contact_signal = pyqtSignal()
    auth_signal = pyqtSignal(int, dict)


SIGNAL = SenderObject()
