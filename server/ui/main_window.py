from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Кнопка выхода
        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        # Кнопка обновить список клиентов
        # self.refresh_button = QAction('Обновить список', self)

        # Кнопка настроек сервера
        self.config_btn = QAction('Settings', self)

        # Кнопка вывести историю сообщений
        self.show_history_button = QAction('History', self)

        # Статусбар
        self.statusBar()

        # Тулбар
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        # self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)

        # Настройки геометрии основного окна
        # Поскольку работать с динамическими размерами мы не умеем, и мало времени на изучение, размер окна фиксирован.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Python messenger (server side)')

        # Надпись о том, что ниже список подключённых клиентов
        self.label = QLabel('Active sessions:', self)
        self.label.setFixedSize(240, 25)
        self.label.move(10, 25)

        # Окно со списком подключённых клиентов.
        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 45)
        self.active_clients_table.setFixedSize(780, 400)

        # Последним параметром отображаем окно.
        self.show()
