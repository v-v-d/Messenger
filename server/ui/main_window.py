from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Кнопка выхода
        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        # TODO: Убрать обновление по кнопке, сделать обновление через созданные триггеры
        self.refresh_button = QAction('Refresh', self)

        # Кнопка настроек сервера
        self.config_btn = QAction('Settings', self)

        # Кнопка вывести историю сообщений
        self.show_history_button = QAction('History', self)

        # Статусбар
        self.statusBar()

        # Тулбар
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)
        self.toolbar.addAction(self.refresh_button)

        # Настройки геометрии основного окна
        # Поскольку работать с динамическими размерами мы не умеем, и мало времени на изучение, размер окна фиксирован.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Python messenger (server side)')

        # Надпись о том, что ниже список подключённых клиентов
        self.label = QLabel('Active sessions:', self)
        self.label.setFixedSize(240, 25)
        self.label.move(10, 25)

        # Окно со списком подключённых клиентов.
        self.connections_table = QTableView(self)
        self.connections_table.move(10, 45)
        self.connections_table.setFixedSize(780, 400)
