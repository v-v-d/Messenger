from PyQt5.QtWidgets import QPushButton, QTableView, QDialog


class ClientStatsWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Настройки окна:
        self.setWindowTitle('Clients stats')
        self.setFixedSize(600, 700)

        # Кнапка закрытия окна
        self.close_button = QPushButton('Close', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close_and_destroy)
        # self.close_button.clicked.connect(self.close)

        # Лист с собственно историей
        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

    def close_and_destroy(self):
        self.close()
        self.history_table.destroy()

