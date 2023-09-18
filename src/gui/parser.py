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
        self.task = 'request'
        self.check_loaded = False
        self.check_error = False
        
    def get_cadastral_numbers(self) -> list[CadastralNumber] | None:
        if self.check_loaded and self.check_error:
            return CadastralNumber.select().where((CadastralNumber.status == 'loaded') | (CadastralNumber.status == 'error'))
        if self.check_loaded:
            return CadastralNumber.select().where(CadastralNumber.status == 'loaded')
        if self.check_error:
            return CadastralNumber.select().where(CadastralNumber.status == 'error')
        return None

    def run(self):
        match self.task:
            case 'request':
                cadastral_numbers = self.get_cadastral_numbers()
                if not cadastral_numbers:
                    return
                self.started.emit(cadastral_numbers.count())
                for num, cadastral_number in enumerate(cadastral_numbers):
                    cadastral_number.status = self.parser.request_EGRN(cadastral_number.cadastral_number)
                    cadastral_number.save()
                    self.progress.emit(num + 1)
            case 'collect':
                cadastral_numbers = CadastralNumber.select().where(CadastralNumber.status == 'sent')
                if not cadastral_numbers:
                    return
                self.started.emit(cadastral_numbers.count())
                for num, cadastral_number in enumerate(cadastral_numbers):
                    cadastral_number.status = self.parser.collect_EGRN(cadastral_number.cadastral_number)
                    cadastral_number.save()
                    self.progress.emit(num + 1)
        self.finished.emit()
