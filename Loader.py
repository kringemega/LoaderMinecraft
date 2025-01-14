from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
import subprocess
import requests
import time
import os
IGNORED_MODULES = []
import ctypes


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("th32ModuleID", ctypes.c_ulong),
        ("th32ProcessID", ctypes.c_ulong),
        ("GlblcntUsage", ctypes.c_ulong),
        ("ProccntUsage", ctypes.c_ulong),
        ("modBaseAddr", ctypes.POINTER(ctypes.c_byte)),
        ("modBaseSize", ctypes.c_ulong),
        ("hModule", ctypes.c_void_p),
        ("szModule", ctypes.c_char * 256),
        ("szExePath", ctypes.c_char * 260)
    ]


def detect_debugger():

    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        print("Debugger detected! Terminating the program.")
        time.sleep(2)
        os._exit(1)


def check_for_dlls(decompilers_and_dlls):
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Module32First = ctypes.windll.kernel32.Module32First
    Module32Next = ctypes.windll.kernel32.Module32Next
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    TH32CS_SNAPMODULE = 0x00000008
    INVALID_HANDLE_VALUE = -1

    for pid in get_process_ids():
        hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid)
        if hModuleSnap == INVALID_HANDLE_VALUE:
            continue

        module_entry = MODULEENTRY32()
        module_entry.dwSize = ctypes.sizeof(MODULEENTRY32)

        if Module32First(hModuleSnap, ctypes.byref(module_entry)):
            while True:
                module_name = module_entry.szModule.decode("utf-8")
                for decompiler, dlls in decompilers_and_dlls.items():
                    if module_name in dlls:
                        print(f"Detected {module_name} from {decompiler}. Terminating.")
                        CloseHandle(hModuleSnap)
                        os._exit(1)

                if not Module32Next(hModuleSnap, ctypes.byref(module_entry)):
                    break

        CloseHandle(hModuleSnap)


def get_process_ids():
    process_ids = (ctypes.c_ulong * 1024)()
    bytes_returned = ctypes.c_ulong()

    EnumProcesses = ctypes.windll.psapi.EnumProcesses
    if not EnumProcesses(ctypes.byref(process_ids), ctypes.sizeof(process_ids), ctypes.byref(bytes_returned)):
        return []

    count = bytes_returned.value // ctypes.sizeof(ctypes.c_ulong)
    return process_ids[:count]


if __name__ == "__main__":
    decompilers_and_dlls = {
        "IDA Pro": ["ida.dll", "ida64.dll", "idapython.dll"],
        "Ghidra": ["ghidra_9.2.4.dll"],
        "dnSpy": ["dnlib.dll", "Mono.Cecil.dll"],
        "Decompiler.NET": ["Decompiler.NET.dll"],
        "Hopper": ["hopper.dll"],
    }

    detect_debugger()
    check_for_dlls(decompilers_and_dlls)


class Ui_InsaneLoader(object):
    def setupUi(self, InsaneLoader):
        InsaneLoader.setObjectName("InsaneLoader")
        InsaneLoader.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        InsaneLoader.setFixedSize(240, 300)

        self.oldPos = None  # For window dragging

        background_image = QtGui.QPixmap(r"C:\Users\User\Music\1017168.jpg")
        scaled_image = background_image.scaled(InsaneLoader.size(), QtCore.Qt.KeepAspectRatioByExpanding)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_image))
        InsaneLoader.setPalette(palette)

        self.closeButton = QtWidgets.QPushButton(InsaneLoader)
        self.closeButton.setGeometry(QtCore.QRect(210, 5, 25, 25))
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 100);
            }
        """)
        self.closeButton.setText("×")
        self.closeButton.clicked.connect(InsaneLoader.close)

        # Minimize Button
        self.minimizeButton = QtWidgets.QPushButton(InsaneLoader)
        self.minimizeButton.setGeometry(QtCore.QRect(180, 5, 25, 25))
        self.minimizeButton.setObjectName("minimizeButton")
        self.minimizeButton.setStyleSheet("""
             QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
            }
        """)
        self.minimizeButton.setText("−")
        self.minimizeButton.clicked.connect(InsaneLoader.showMinimized)

        # Label for the image
        self.label = QtWidgets.QLabel(InsaneLoader)
        self.label.setGeometry(QtCore.QRect(40, 20, 161, 161))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(r"C:\Users\User\Music\1017168.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.username_input = QtWidgets.QLineEdit(InsaneLoader)
        self.username_input.setGeometry(QtCore.QRect(40, 190, 160, 22))
        self.username_input.setObjectName("username_input")
        self.username_input.setPlaceholderText("Логин")
        self.username_input.setAlignment(QtCore.Qt.AlignCenter)
        self.username_input.setStyleSheet("""
            QLineEdit {
                font-weight: bold;
                font-size: 12px;
                background-color: transparent;
                border: none;
                color: white;
            }
            QLineEdit:focus {
                border: none;
            }
        """)

        # Password input field
        self.password_input = QtWidgets.QLineEdit(InsaneLoader)
        self.password_input.setGeometry(QtCore.QRect(40, 220, 160, 22))
        self.password_input.setObjectName("password_input")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.password_input.setStyleSheet("""
            QLineEdit {
                font-weight: bold;
                font-size: 12px;
                background-color: transparent;
                border: none;
                color: white;
            }
            QLineEdit:focus {
                border: none;
            }
        """)

        # Login button
        self.pushButton = QtWidgets.QPushButton(InsaneLoader)
        self.pushButton.setGeometry(QtCore.QRect(80, 260, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 10px;
                padding: 5px 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                 background-color: #2471a3;
            }
        """)

        self.pushButton.clicked.connect(self.login_action)
        self.InsaneLoader = InsaneLoader

        self.retranslateUi(InsaneLoader)
        QtCore.QMetaObject.connectSlotsByName(InsaneLoader)

        InsaneLoader.mousePressEvent = self.mousePressEvent
        InsaneLoader.mouseMoveEvent = self.mouseMoveEvent
        InsaneLoader.mouseReleaseEvent = self.mouseReleaseEvent
## хвид
    def check_hwid(self):
        hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        r = requests.get('Ваш пастебин')

        try:
            if hwid in r.text:
                return True
            else:
                print('Ошибка, данных hwid не был найден в базе данных')
                print(f'HWID: {hwid}')
                time.sleep(5)
                os._exit(1)
        except:
            print('Ошибка, не удаётся соединится с базой данных')
            time.sleep(5)
            os._exit(1)
## гит на логин и пароль
    LOGIN_URL = "ваш гит"
    PASSWORD_URL = "ваш гит"

    def check_data(self, input_value, url, data_type):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.text.splitlines()

            if input_value in data:
                return True
            else:
                print("Неправильный пароль или логин")
                return False
        except Exception as e:
            print(f"Ошибка при соединении с базой данных: {e}")
            return False

    def login_action(self):
        if not self.check_hwid():
            return
        login = self.username_input.text()
        password = self.password_input.text()
        if self.check_data(login, self.LOGIN_URL, "login") and self.check_data(password, self.PASSWORD_URL, "password"):
            self.open_new_window()

    def open_new_window(self):
        self.new_window = QtWidgets.QMainWindow()
        self.new_ui = Ui_NewWindow()
        self.new_ui.setupUi(self.new_window)
        self.new_window.show()
        self.InsaneLoader.close()  # Close login window

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.oldPos:
            delta = event.globalPos() - self.oldPos
            source = event.source()
            if isinstance(source, QtWidgets.QWidget):
                source.move(source.x() + delta.x(), source.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.oldPos = None

    def retranslateUi(self, InsaneLoader):
        _translate = QtCore.QCoreApplication.translate
        InsaneLoader.setWindowTitle(_translate("InsaneLoader", "Авторизация"))
        self.pushButton.setText(_translate("InsaneLoader", "Войти"))


class Ui_NewWindow(object):
    def setupUi(self, NewWindow):
        self.NewWindow = NewWindow
        NewWindow.setObjectName("NewWindow")
        NewWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        NewWindow.resize(450, 300)


        background_image = QtGui.QPixmap(r"C:\Users\User\Downloads\bluered.png")
        scaled_image = background_image.scaled(NewWindow.size(), QtCore.Qt.KeepAspectRatioByExpanding)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_image))
        NewWindow.setPalette(palette)

        self.closeButton = QtWidgets.QPushButton(NewWindow)
        self.closeButton.setGeometry(QtCore.QRect(420, 5, 25, 25))
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 100);
            }
        """)
        self.closeButton.setText("×")
        self.closeButton.clicked.connect(NewWindow.close)

        self.minimizeButton = QtWidgets.QPushButton(NewWindow)
        self.minimizeButton.setGeometry(QtCore.QRect(390, 5, 25, 25))
        self.minimizeButton.setObjectName("minimizeButton")
        self.minimizeButton.setStyleSheet("""
             QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
            }
        """)
        self.minimizeButton.setText("−")
        self.minimizeButton.clicked.connect(NewWindow.showMinimized)

        self.label = QtWidgets.QLabel(NewWindow)
        self.label.setGeometry(QtCore.QRect(200, 40, 230, 70))  # Moved text down more
        self.label.setObjectName("label")
        self.label.setText(
            "InsaneV2 - это ваше ПО которое будет помогать вам в игре.\nСтаньте непобедимым благодаря InsaneV2! и доминируйте над всеми серверами.")
        self.label.setStyleSheet("color: white; font-size: 12px; text-align: right;")
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)  # Enable word wrap

        self.launchButton = QtWidgets.QPushButton(NewWindow)
        self.launchButton.setGeometry(QtCore.QRect(320, 230, 100, 40))
        self.launchButton.setObjectName("launchButton")
        self.launchButton.setText("Запустить")
        self.launchButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """)
        # Label above the button
        self.label_above_button = QtWidgets.QLabel(NewWindow)
        self.label_above_button.setGeometry(QtCore.QRect(300, 200, 130, 20))
        self.label_above_button.setObjectName("labelAboveButton")
        self.label_above_button.setText("Нажмите для запуска")
        self.label_above_button.setStyleSheet("color: white; font-size: 10px; text-align: center;")
        self.label_above_button.setAlignment(QtCore.Qt.AlignCenter)
        self.launchButton.clicked.connect(self.show_loading_animation)


        self.webView = QWebEngineView(NewWindow)
        self.webView.setGeometry(QtCore.QRect(20, 20, 410, 260))
        self.webView.setObjectName("webView")
        self.webView.hide()

        NewWindow.mousePressEvent = self.mousePressEvent
        NewWindow.mouseMoveEvent = self.mouseMoveEvent
        NewWindow.mouseReleaseEvent = self.mouseReleaseEvent
        self.imageLabel = QtWidgets.QLabel(NewWindow)
        self.imageLabel.setGeometry(QtCore.QRect(30, 60, 170, 170))
        self.imageLabel.setPixmap(QtGui.QPixmap(r"C:\Users\User\Downloads\acetone-20241227-163440-411.png"))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setObjectName("imageLabel")
        self.webView = QWebEngineView(NewWindow)
        self.webView.setGeometry(NewWindow.rect())
        self.webView.setObjectName("webView")
        self.webView.hide()

        self.closeButton.setParent(NewWindow)
        self.minimizeButton.setParent(NewWindow)

        self.launchButton.clicked.connect(self.show_web_view)
    def show_loading_animation(self):
        html_path = r"C:\Users\User\Desktop\InsaneProtect\index.html"
        if os.path.exists(html_path):
            self.webView.load(QtCore.QUrl.fromLocalFile(html_path))
            self.webView.show()
        else:
            print(f"File not found: {html_path}")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.oldPos:
            delta = event.globalPos() - self.oldPos
            source = event.source()
            if isinstance(source, QtWidgets.QWidget):
                source.move(source.x() + delta.x(), source.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.oldPos = None

    def show_web_view(self):
        self.imageLabel.hide()
        self.label.hide()
        self.label_above_button.hide()
        self.launchButton.hide()

        self.webView.setGeometry(self.NewWindow.rect())
        self.webView.load(QtCore.QUrl.fromLocalFile(r"C:\Users\User\Desktop\InsaneProtect\index.html"))
        self.webView.show()

        self.closeButton.raise_()
        self.minimizeButton.raise_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    InsaneLoader = QtWidgets.QWidget()
    ui = Ui_InsaneLoader()
    ui.setupUi(InsaneLoader)
    InsaneLoader.show()
    sys.exit(app.exec_())
