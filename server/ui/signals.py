from PyQt5.QtCore import pyqtSignal, QObject


class SenderObject(QObject):
    active_client_signal = pyqtSignal()


SIGNAL = SenderObject()
