from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QLineEdit, QFileDialog


class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setFixedSize(365, 260)
        self.setWindowTitle('Server config')

        # Надпись о файле базы данных:
        self.db_path_label = QLabel('Path to database: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)

        # Строка с путём базы
        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 30)
        # self.db_path.setReadOnly(True)

        # Кнопка выбора пути.
        self.db_path_select = QPushButton('Browse...', self)
        self.db_path_select.move(275, 28)

        # Окно выбора папки с БД.
        self.dialog = QFileDialog(self)

        self.db_path_select.clicked.connect(self.open_file_dialog)

        # Метка с именем поля файла базы данных
        self.db_file_label = QLabel('Database filename: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)

        # Поле для ввода имени файла
        self.db_file = QLineEdit(self)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)

        # Метка с номером порта
        self.port_label = QLabel('Port number: ', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        # Поле для ввода номера порта
        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        # Метка с адресом для соединений
        self.host_label = QLabel('IP address: ', self)
        self.host_label.move(10, 148)
        self.host_label.setFixedSize(180, 15)

        # Метка с напоминанием о пустом поле.
        self.host_label_note = QLabel('(blank for accepting from any addresses)', self)
        self.host_label_note.move(10, 168)
        self.host_label_note.setFixedSize(500, 30)

        # Поле для ввода ip
        self.host = QLineEdit(self)
        self.host.move(200, 148)
        self.host.setFixedSize(150, 20)

        # Кнопка сохранения настроек
        self.save_btn = QPushButton('Save', self)
        self.save_btn.move(190, 220)

        # Кнапка закрытия окна
        self.close_button = QPushButton('Close', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.clear_close_and_destroy)

    def open_file_dialog(self):
        path = self.dialog.getExistingDirectory()
        path = path.replace('/', '\\')
        self.db_path.clear()
        self.db_path.insert(path)

    def clear_close_and_destroy(self):
        self.db_path.clear()
        self.db_file.clear()
        self.port.clear()
        self.host.clear()
        self.close()
        self.destroy()
