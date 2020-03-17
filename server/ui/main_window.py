from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        exitAction = QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        self.config_btn = QAction('Settings', self)

        self.show_history_button = QAction('History', self)

        self.statusBar()

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Python messenger (server side)')

        self.label = QLabel('Active sessions:', self)
        self.label.setFixedSize(240, 25)
        self.label.move(10, 25)

        self.connections_table = QTableView(self)
        self.connections_table.move(10, 45)
        self.connections_table.setFixedSize(780, 400)
