import socket
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPalette, QColor
import json
import _thread
import datetime


class ConnectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.lbl1 = QLabel(self)
        self.lbl1.setText("Enter your nickname")
        self.lbl1.setGeometry(40, 20, 300, 25)
        self.lbl1.setFont(QFont("Times", 12, QFont.Decorative))

        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(40, 50, 320, 50)
        self.name_input.setFont(QFont("Times", 14, QFont.Decorative))

        self.lbl1 = QLabel(self)
        self.lbl1.setText("Enter server's address")
        self.lbl1.setGeometry(40, 120, 300, 25)
        self.lbl1.setFont(QFont("Times", 12, QFont.Decorative))

        self.input = QLineEdit(self)
        self.input.setGeometry(40, 150, 320, 50)
        self.input.setFont(QFont("Times", 14, QFont.Decorative))

        self.lbl2 = QLabel(self)
        self.lbl2.setText('or choose from list')
        self.lbl2.setGeometry(40, 220, 400, 25)
        self.lbl2.setFont(QFont("Times", 12, QFont.Decorative))

        self.combo = QComboBox(self)
        self.combo.addItems(["localhost"])
        self.combo.setFont(QFont("Times", 12, QFont.Decorative))
        self.combo.setGeometry(125, 250, 150, 40)

        self.enter_btn = QPushButton('Join', self)
        self.enter_btn.setFont(QFont("Times", 14, QFont.Decorative))
        self.enter_btn.setGeometry(100, 320, 200, 50)
        self.enter_btn.clicked.connect(self.get_address)

        self.quit_btn = QPushButton('Exit', self)
        self.quit_btn.setGeometry(125, 400, 150, 50)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.resize(400, 500)
        self.center()
        self.setWindowTitle('Connect')
        self.show()

    def get_address(self):
        if not self.name_input.text().strip():
            self.statusBar().showMessage('Enter nickname')
            return
        if self.input.text() == '' or self.input.text() is None:
            address = self.combo.currentText()
        else:
            address = self.input.text()
        try:
            self.modal_window = MessageWindow(address=address, nickname=self.name_input.text())
            self.modal_window.show()
            self.hide()
        except ConnectionRefusedError:
            self.statusBar().showMessage('Server is unavailable')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MessageWindow(QMainWindow):
    def __init__(self, address, nickname):
        super().__init__()
        self.nickname = nickname
        self._socket = socket.socket()
        self.address = address
        self._socket.connect((self.address, 9000))
        self._socket.send(self.make_message('Joined', 1).encode('utf-8'))
        _thread.start_new_thread(listen, (self._socket,))
        self.init_ui()

    def init_ui(self):
        self.quit_btn = QPushButton('Exit', self)
        self.quit_btn.setGeometry(620, 330, 150, 50)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.input = QTextEdit(self)
        self.input.setGeometry(30, 30, 740, 200)
        self.input.setFont(QFont("Times", 16, QFont.Decorative))

        self.enter_btn = QPushButton('Send message', self)
        self.enter_btn.setGeometry(200, 250, 400, 50)
        self.enter_btn.setFont(QFont("Times", 14, QFont.Decorative))
        self.enter_btn.clicked.connect(self.send_message)
        self.enter_btn.setShortcut('Enter')

        self.resize(800, 400)
        self.center()
        self.setWindowTitle(f'Chat - {self.nickname}')
        self.show()

    def make_message(self, message, status):
        return json.dumps({'from': self.nickname, 'message': message, 'status': status})

    def send_message(self):
        message = self.input.toPlainText()
        self.input.clear()
        if message.strip():
            try:
                self._socket.send(self.make_message(message, 2).encode('utf-8'))
            except:
                self.statusBar().showMessage('Server has gone away')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def listen(sock):
    while True:
        data = sock.recv(1024).decode('utf-8')
        if not data:
            continue
        else:
            print(data)


# name = input('Your nickname >> ')
# sock = socket.socket()
# try:
#     sock.connect(('127.0.0.2', 9000))
#     _thread.start_new_thread(listen, (sock,))
#     sock.send(make_message(name, '').encode('utf-8'))
#     while True:
#         try:
#             print("Enter your message")
#             mess = input()
#             sock.send(make_message(name, mess).encode('utf-8'))
#             # print(sock.recv(1024).decode('utf-8'))
#         except ConnectionResetError:
#             print("Server has gone away")
#             break
# except ConnectionRefusedError:
#     print("Server is unavailable. Please, try later")
# sock.connect(('18.217.88.63', 9000))
# sock.connect(('localhost', 9000))
app = QApplication(sys.argv)
connector = ConnectWindow()
sys.exit(app.exec_())
