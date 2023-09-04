from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal
from ..parser import Parser
from ..database.models import CadastralNumber

class ParserThread(QThread):
    started = pyqtSignal(int)
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.cadastral_numbers: list[CadastralNumber] = CadastralNumber.select().where(CadastralNumber.status == 'loaded')
        self.parser = Parser()
        self.parser.login()

    def run(self):
        self.started.emit(self.cadastral_numbers.count())
        if self.cadastral_numbers.count() == 0:
            return self.finished.emit()
        for num, cadastral_number in enumerate(self.cadastral_numbers):
            try:
                self.parser.request_EGRN(cadastral_number.cadastral_number)
                cadastral_number.status = 'sent'
            except Exception as e:
                cadastral_number.status = 'error'
                with open('exceptions.txt', 'a', encoding='utf-8') as logfile:
                    logfile.write(f'[{datetime.now()}] ERROR: {e}')
            cadastral_number.save()
            self.progress.emit(num + 1)
        self.finished.emit()
