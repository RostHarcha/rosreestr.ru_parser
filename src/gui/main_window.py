from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from .ui import Ui_Main_window
from ..database.models import CadastralNumber
from .parser import ParserThread

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Парсер rosreestr.ru')
        self.ui = Ui_Main_window()
        self.ui.setupUi(self)
        self.setup_buttons()
        self.update_indicators()

    def setup_buttons(self):
        self.disable_parser_buttons()
        self.ui.button_launch_driver.clicked.connect(self.launch_driver)
        self.ui.button_send_requests.clicked.connect(self.send_requests)
        self.ui.button_load_input_filepath.clicked.connect(self.import_numbers)
        self.ui.button_get_responds.clicked.connect(self.get_responds)
        self.ui.clear_stat.clicked.connect(self.clear_stat)

    def update_indicators(self):
        values = CadastralNumber.get_statuses()
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(values.total)
        for n, num in enumerate(CadastralNumber.select()):
            self.ui.tableWidget.setItem(n, 0, QTableWidgetItem(num.cadastral_number))
            self.ui.tableWidget.setItem(n, 1, QTableWidgetItem(num.created_at))
            self.ui.tableWidget.setItem(n, 2, QTableWidgetItem(num.status))
        def set_value(label, value: int):
            percent = 0 if values.total == 0 else int(value / values.total * 100)
            label.setText(f'{value}\t({percent}%)')
        set_value(self.ui.label_nums_total_value, values.total)
        set_value(self.ui.label_nums_loaded_value, values.loaded)
        set_value(self.ui.label_nums_sent_value, values.sent)
        set_value(self.ui.label_nums_received_value, values.received)
        set_value(self.ui.label_nums_error_value, values.error)

    def update_progressBar(self, value: int):
        self.ui.progressBar.setValue(value)

    def enable_parser_buttons(self):
        self.ui.button_send_requests.setEnabled(True)
        self.ui.button_get_responds.setEnabled(True)

    def disable_parser_buttons(self):
        self.ui.button_send_requests.setEnabled(False)
        self.ui.button_get_responds.setEnabled(False)

    def parser_started(self, cadastral_numbers_count: int):
        self.disable_parser_buttons()
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(cadastral_numbers_count)
        
    def clear_stat(self):
        for num in CadastralNumber.select():
            num.delete_instance()
        self.update_indicators()

    def parser_finished(self):
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue(0)
        self.update_indicators()
        self.enable_parser_buttons()


    def launch_driver(self):
        self.parser = ParserThread()
        self.enable_parser_buttons()
        self.parser.started.connect(self.parser_started)
        self.parser.finished.connect(self.parser_finished)
        self.parser.progress.connect(self.update_progressBar)

    def send_requests(self):
        self.parser.check_loaded = self.ui.check_loaded.isChecked()
        self.parser.check_error = self.ui.check_error.isChecked()
        if not (self.parser.check_loaded or self.parser.check_error):
            self.problem('[ ] Загружено, [ ] Ошибка: нужно выбрать хотя бы одно.')
            return
        self.parser.task = 'request'
        self.parser.start()
        self.problem()
    
    def get_responds(self):
        try:
            self.parser.task = 'collect'
            self.parser.start()
            self.problem()
        except:
            self.problem('Не удалось запустить Получение ответов.')

    def problem(self, message: str = None):
        if message is None:
            self.ui.label_problems.setStyleSheet('color: green;')
            self.ui.label_problems.setText('Проблемы не обнаружены.')
        else:
            self.ui.label_problems.setStyleSheet('color: red;')
            self.ui.label_problems.setText(message)

    def import_numbers(self):
        filepath = self.ui.input_input_filepath.text()
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                while line := file.readline():
                    try:
                        CadastralNumber.create(
                            cadastral_number=line.rstrip(),
                            status='loaded'
                        )
                    except:
                        pass
            self.update_indicators()
            self.problem()
        except:
            self.problem(f'Не удается открыть файл "{filepath}". Проверьте поле "Путь к файлу".')
