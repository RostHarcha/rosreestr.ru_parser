# Form implementation generated from reading ui file '.\gui\ui\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(541, 258)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        MainWindow.setWindowTitle("Парсер rosreestr.ru by @rostislaww")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.auth_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.auth_groupBox.setGeometry(QtCore.QRect(10, 10, 291, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auth_groupBox.setFont(font)
        self.auth_groupBox.setObjectName("auth_groupBox")
        self.ESIA_login = QtWidgets.QLineEdit(parent=self.auth_groupBox)
        self.ESIA_login.setGeometry(QtCore.QRect(10, 21, 171, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ESIA_login.setFont(font)
        self.ESIA_login.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ESIA_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ESIA_login.setClearButtonEnabled(False)
        self.ESIA_login.setObjectName("ESIA_login")
        self.ESIA_password = QtWidgets.QLineEdit(parent=self.auth_groupBox)
        self.ESIA_password.setGeometry(QtCore.QRect(10, 51, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ESIA_password.setFont(font)
        self.ESIA_password.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ESIA_password.setText("")
        self.ESIA_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ESIA_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ESIA_password.setObjectName("ESIA_password")
        self.ESIA_login_button = QtWidgets.QPushButton(parent=self.auth_groupBox)
        self.ESIA_login_button.setGeometry(QtCore.QRect(10, 80, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ESIA_login_button.setFont(font)
        self.ESIA_login_button.setObjectName("ESIA_login_button")
        self.line = QtWidgets.QFrame(parent=self.auth_groupBox)
        self.line.setGeometry(QtCore.QRect(180, 20, 20, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.ESIA_loginQR_button = QtWidgets.QPushButton(parent=self.auth_groupBox)
        self.ESIA_loginQR_button.setGeometry(QtCore.QRect(200, 20, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ESIA_loginQR_button.setFont(font)
        self.ESIA_loginQR_button.setObjectName("ESIA_loginQR_button")
        self.ESIA_loginESigrature_button = QtWidgets.QPushButton(parent=self.auth_groupBox)
        self.ESIA_loginESigrature_button.setGeometry(QtCore.QRect(200, 60, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ESIA_loginESigrature_button.setFont(font)
        self.ESIA_loginESigrature_button.setObjectName("ESIA_loginESigrature_button")
        self.parsing_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.parsing_groupBox.setGeometry(QtCore.QRect(10, 130, 291, 81))
        self.parsing_groupBox.setObjectName("parsing_groupBox")
        self.start_requests_button = QtWidgets.QPushButton(parent=self.parsing_groupBox)
        self.start_requests_button.setGeometry(QtCore.QRect(10, 20, 271, 23))
        self.start_requests_button.setObjectName("start_requests_button")
        self.start_downloading_button = QtWidgets.QPushButton(parent=self.parsing_groupBox)
        self.start_downloading_button.setGeometry(QtCore.QRect(10, 50, 271, 23))
        self.start_downloading_button.setObjectName("start_downloading_button")
        self.data_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.data_groupBox.setGeometry(QtCore.QRect(310, 10, 201, 201))
        self.data_groupBox.setObjectName("data_groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.data_groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 50, 185, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.downloaded_count = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.downloaded_count.setObjectName("downloaded_count")
        self.gridLayout.addWidget(self.downloaded_count, 3, 1, 1, 1)
        self.new_count = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.new_count.setObjectName("new_count")
        self.gridLayout.addWidget(self.new_count, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.sent_count = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.sent_count.setObjectName("sent_count")
        self.gridLayout.addWidget(self.sent_count, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.error_count = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.error_count.setObjectName("error_count")
        self.gridLayout.addWidget(self.error_count, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.current_cadastral_number = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.current_cadastral_number.setText("")
        self.current_cadastral_number.setObjectName("current_cadastral_number")
        self.gridLayout.addWidget(self.current_cadastral_number, 4, 1, 1, 1)
        self.clear_data_button = QtWidgets.QPushButton(parent=self.data_groupBox)
        self.clear_data_button.setGeometry(QtCore.QRect(110, 20, 81, 23))
        self.clear_data_button.setObjectName("clear_data_button")
        self.load_data_button = QtWidgets.QPushButton(parent=self.data_groupBox)
        self.load_data_button.setGeometry(QtCore.QRect(10, 20, 81, 23))
        self.load_data_button.setObjectName("load_data_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 541, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(parent=MainWindow)
        self.action.setObjectName("action")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.auth_groupBox.setTitle(_translate("MainWindow", "Авторизация"))
        self.ESIA_login.setPlaceholderText(_translate("MainWindow", "Телефон / Email / СНИЛС"))
        self.ESIA_password.setPlaceholderText(_translate("MainWindow", "Пароль"))
        self.ESIA_login_button.setText(_translate("MainWindow", "Войти"))
        self.ESIA_loginQR_button.setText(_translate("MainWindow", "QR-код"))
        self.ESIA_loginESigrature_button.setText(_translate("MainWindow", "Эл. подпись"))
        self.parsing_groupBox.setTitle(_translate("MainWindow", "Парсинг"))
        self.start_requests_button.setText(_translate("MainWindow", "Начать заказ"))
        self.start_downloading_button.setText(_translate("MainWindow", "Начать скачивание"))
        self.data_groupBox.setTitle(_translate("MainWindow", "Данные"))
        self.downloaded_count.setText(_translate("MainWindow", "0"))
        self.new_count.setText(_translate("MainWindow", "0"))
        self.label_6.setText(_translate("MainWindow", "Ошибка"))
        self.sent_count.setText(_translate("MainWindow", "0"))
        self.label_5.setText(_translate("MainWindow", "Отправлено"))
        self.label_3.setText(_translate("MainWindow", "Новые"))
        self.error_count.setText(_translate("MainWindow", "0"))
        self.label.setText(_translate("MainWindow", "Скачано"))
        self.label_2.setText(_translate("MainWindow", "Текущий"))
        self.clear_data_button.setText(_translate("MainWindow", "Очистить"))
        self.load_data_button.setText(_translate("MainWindow", "Загрузить..."))
        self.action.setText(_translate("MainWindow", "Тест"))