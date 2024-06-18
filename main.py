import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow

def get_window():
    window = MainWindow()
    window.show()
    return window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = get_window()
    app.exec()
