import sys
from logging import getLogger
from logging.config import dictConfig

from PyQt5.QtWidgets import QApplication, QMessageBox

from descriptors import HostValidator, PortValidator
from log.log_config import LOGGING
from ui.client_stats_window import ClientStatsWindow
from ui.config_window import ConfigWindow
from ui.main_window import MainWindow
from ui.utils import get_connections_table, get_client_stats_table
from utils import get_config_from_yaml, write_config_to_yaml


class GUIApplication:
    host = HostValidator()
    port = PortValidator()

    def __init__(self):
        self.config_window = None
        self.stat_window = None
        self.main_window = None
        self.config = get_config_from_yaml()

        dictConfig(LOGGING)
        self.logger = getLogger('server')

    def __enter__(self):
        self.logger.info('Server GUI was rendered.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.critical(f'GUI closed with error: {exc_type}: {exc_val}')
        else:
            self.logger.info('GUI closed.')
        return True

    def render(self):
        app = QApplication(sys.argv)
        self.config_window = ConfigWindow()
        self.stat_window = ClientStatsWindow()
        self.main_window = MainWindow()
        self.show_main_window()
        app.exec_()

    def show_main_window(self):
        self.main_window.statusBar().showMessage('Server running')
        self.connect_main_window_buttons()
        self.render_connections_table()
        self.main_window.show()

    def connect_main_window_buttons(self):
        # TODO: Убрать обновление по кнопке, сделать обновление через созданные триггеры
        self.main_window.refresh_button.triggered.connect(self.render_connections_table)

        self.main_window.show_history_button.triggered.connect(self.show_client_stats_window)
        self.main_window.config_btn.triggered.connect(self.show_config_window)

    def render_connections_table(self):
        self.main_window.connections_table.setModel(get_connections_table())
        self.main_window.connections_table.resizeColumnsToContents()
        self.main_window.connections_table.resizeRowsToContents()

    def show_client_stats_window(self):
        self.stat_window.history_table.setModel(get_client_stats_table())
        self.stat_window.history_table.resizeColumnsToContents()
        self.stat_window.history_table.resizeRowsToContents()
        self.stat_window.show()

    def show_config_window(self):
        if self.config:
            self.config_window.db_path.insert(self.config.get('db_path'))
            self.config_window.db_file.insert(self.config.get('db_file'))
            self.config_window.port.insert(self.config.get('db_port'))
            self.config_window.host.insert(self.config.get('db_host'))

        self.config_window.show()
        self.config_window.save_btn.clicked.connect(self.save_config_to_file)

    def save_config_to_file(self):
        message = QMessageBox()
        errors = self.get_validation_errors()
        if errors:
            err = ''.join([f'{error}\n'.capitalize() for error in errors])
            message.warning(self.config_window, 'Error', err)
        else:
            self.config['db_path'] = self.config_window.db_path.text()
            self.config['db_file'] = self.config_window.db_file.text()
            self.config['port'] = self.port
            self.config['host'] = self.host
            write_config_to_yaml(self.config)
            message.information(self.config_window, 'OK', 'Config is set up!')

    def get_validation_errors(self):
        errors = list()
        try:
            self.host = self.config_window.host.text()
        except ValueError as error:
            errors.append(error)
        try:
            self.port = int(self.config_window.port.text())
        except ValueError as error:
            errors.append(error)

        return errors
