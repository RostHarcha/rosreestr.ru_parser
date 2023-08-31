import sys
from PyQt6.QtWidgets import QApplication
from src import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = gui.MainWindow()
    window.show()
    app.exec()
