from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from .ui.main_window import Ui_MainWindow
from .parser import ParserThread, ParserTask

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_buttons()
        self.setup_parser()
    
    def setup_buttons(self):
        self.ui.ESIA_login_button.clicked.connect(self.esia_login)
        self.ui.ESIA_loginQR_button.clicked.connect(self.esia_login_qrCode)
        self.ui.ESIA_loginESigrature_button.clicked.connect(self.esia_login_ESigrature)
        self.ui.load_data_button.clicked.connect(self.load_data)
        self.ui.clear_data_button.clicked.connect(self.clear_data)
        self.ui.start_requests_button.clicked.connect(self.start_requests)
        self.ui.start_downloading_button.clicked.connect(self.start_download)
    
    def setup_parser(self):
        self.parser = ParserThread(self)
        self.parser.indicators.connect(self.update_indicators)
        self.parser.current_cadastral_number.connect(self.update_current_cadastral_number)
        self.parser.update_indicators()
    
    def closeEvent(self, a0):
        self.parser.driver.close()
        return super().closeEvent(a0)

    def update_indicators(self, new, sent, error, downloaded):
        self.ui.new_count.setText(str(new))
        self.ui.sent_count.setText(str(sent))
        self.ui.error_count.setText(str(error))
        self.ui.downloaded_count.setText(str(downloaded))
    
    def update_current_cadastral_number(self, value):
        self.ui.current_cadastral_number.setText(value)
    
    def esia_login(self):
        self.parser.ESIA_login = self.ui.ESIA_login.text()
        self.parser.ESIA_password = self.ui.ESIA_password.text()
        self.parser.task = ParserTask.LOGIN
        self.parser.start()
    
    def esia_login_qrCode(self):
        self.parser.task = ParserTask.LOGIN_QR
        self.parser.start()
    
    def esia_login_ESigrature(self):
        self.parser.task = ParserTask.LOGIN_ESIGN
        self.parser.start()
    
    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter="Текст (*.txt)")
        if filename:
            self.parser.data_filename = filename
            self.parser.task = ParserTask.LOAD_DATA
            self.parser.start()
    
    def clear_data(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Вы уверены?')
        dlg.setText('Все данные будут удалены безвозвратно.\nЧтобы отменить, нажмите "Cancel"')
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        dlg.setIcon(QMessageBox.Icon.Warning)
        if dlg.exec() == QMessageBox.StandardButton.Ok:
            self.parser.task = ParserTask.CLEAR_DATA
            self.parser.start()
    
    def start_requests(self):
        self.parser.task = ParserTask.REQUESTS
        self.parser.start()
    
    def start_download(self):
        self.parser.task = ParserTask.DOWNLOAD_DATA
        self.parser.start()
