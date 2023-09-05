from PyQt6.QtCore import QThread, pyqtSignal
from ..parser import Parser
from ..database.models import CadastralNumber

class ParserThread(QThread):
    started = pyqtSignal(int)
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.cadastral_numbers: list[CadastralNumber] = []
        self.parser = Parser()
        self.parser.login()

    def load_cadastral_numbers(self, loaded: bool, error: bool):
        '''Returns None if no results'''
        if not (loaded or error):
            raise
        if loaded and error:
            q = (CadastralNumber.status == 'loaded') | (CadastralNumber.status == 'error')
        elif loaded:
            q = (CadastralNumber.status == 'loaded')
        else:
            q = (CadastralNumber.status == 'error')
        self.cadastral_numbers = CadastralNumber.select().where(q)

    def run(self):
        self.started.emit(self.cadastral_numbers.count())
        if self.cadastral_numbers.count() == 0:
            return self.finished.emit()
        for num, cadastral_number in enumerate(self.cadastral_numbers):
            if self.parser.request_EGRN(cadastral_number.cadastral_number):
                cadastral_number.status = 'sent'
            else:
                cadastral_number.status = 'error'
            cadastral_number.save()
            self.progress.emit(num + 1)
        self.finished.emit()
