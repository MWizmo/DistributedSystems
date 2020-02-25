import socket
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
import json
import os


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
            sock = socket.socket()
            sock.connect((address, 9000))
            sock.send(json.dumps({'from': self.name_input.text(), 'message': 'Connection', 'status': 1}).encode('utf-8'))
            data = json.loads(sock.recv(1024).decode('utf-8'))
            sock.close()
            if data['message'] == 'ok':
                self.modal_window = MessageWindow(address=address, nickname=self.name_input.text())
                self.modal_window.show()
                self.hide()
            else:
                self.statusBar().showMessage('This nickname is busy')
        except ConnectionRefusedError:
            self.statusBar().showMessage('Server is unavailable')
        except Exception as e:
            print(e)
            self.statusBar().showMessage('Error 500')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class BrowserHandler(QObject):
    running = False
    client_func = pyqtSignal(int, str)

    def run(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    continue
                try:
                    data = json.loads(data)
                except:
                    continue
                if data['status'] in [0, 2, 3, 7]:
                    print(data['message'])
                elif data['status'] == 4:
                    print('-' * 22)
                    print('|', 'Users on channel'.center(20), '|', sep='')
                    print('-' * 22)
                    for i, user in enumerate(data['message']):
                        print('|', f'{i + 1}. {user}'.ljust(20), '|', sep='')
                    print('-' * 22)
                elif data['status'] == 5:
                    if data['message'].startswith('ok'):
                        title = '_'.join(data['message'].split('_')[1:-1])
                        room_id = int(data['message'].split('_')[-1])
                        self.client_func.emit(room_id, title)
                    else:
                        self.client_func.emit(-1, '')
                elif data['status'] == 6:
                    if data['message'].startswith('ok'):
                        title = '_'.join(data['message'].split('_')[1:-1])
                        room_id = int(data['message'].split('_')[-1])
                        self.client_func.emit(room_id, title)
                    else:
                        self.client_func.emit(-2, '')
                elif data['status'] == 8:
                    filename = data['message']
                    with self.sock.makefile('rb') as file:
                        while True:
                            raw = file.readline()
                            if not raw:
                                break
                            filename = raw.strip().decode()
                            length = int(file.readline())
                            path = os.path.join('uploads', filename)
                            with open(path, 'wb') as f:
                                while length:
                                    data = file.read(min(length, 100000))
                                    if not data:
                                        break
                                    f.write(data)
                                    length -= len(data)
                            print(f'-- File was uploaded to uploads/{filename} --')
                            break
                elif data['status'] == 80:
                    print("There is no this file in room!")
                elif data['status'] == 9:
                    if data['message']:
                        files = data['message'].split('|')
                        print(f"Files in room '{data['room']}':")
                        for i, file in enumerate(files):
                            print(f'{i+1}. {file}')
                    else:
                        print(f'Room "{data["room"]}" has empty list of files')
            except ConnectionResetError:
                break
            except Exception as e:
                print(e)
                continue


class MessageWindow(QWidget):
    def __init__(self, address, nickname):
        super().__init__()
        self.nickname = nickname
        self._socket = socket.socket()
        self.address = address
        self._socket.connect((self.address, 9000))
        self.thread = QThread()
        self.browserHandler = BrowserHandler()
        self.browserHandler.sock = self._socket
        self.browserHandler.mainWindow = self
        self.browserHandler.moveToThread(self.thread)
        self.browserHandler.client_func.connect(self.add_room)
        self.thread.started.connect(self.browserHandler.run)
        self.thread.start()
        self.send_message('Joined', 2)
        self.init_ui()

    @pyqtSlot(int, str)
    def add_room(self, room_id, title):
        if room_id > -1:
            grid = QGridLayout()
            grid.setSpacing(10)
            input = QTextEdit(self)
            input.setFont(QFont("Times", 16, QFont.Decorative))

            enter_btn = QPushButton('Send message', self)
            enter_btn.setFont(QFont("Times", 14, QFont.Decorative))
            enter_btn.clicked.connect(lambda i: self.send_usual_message(input, room_id))
            enter_btn.setShortcut('Enter')

            user_btn = QPushButton("User's list", self)
            user_btn.clicked.connect(lambda i: self.list_of_users(room_id))

            send_file_btn = QPushButton('Send file', self)
            send_file_btn.clicked.connect(lambda i: self.send_file(room_id))

            look_files_btn = QPushButton('List of files', self)
            look_files_btn.clicked.connect(lambda i: self.look_files(room_id))

            upload_file_btn = QPushButton('Upload file', self)
            upload_file_btn.clicked.connect(lambda i: self.upload_file(room_id))

            grid.addWidget(input, 1, 0, 2, 4)
            grid.addWidget(enter_btn, 3, 1, 1, 2)
            grid.addWidget(user_btn, 4, 0)
            grid.addWidget(send_file_btn, 4, 1)
            grid.addWidget(look_files_btn, 4, 2)
            grid.addWidget(upload_file_btn, 4, 3)
            #grid.addWidget(quit_btn, 4, 3)

            new_chat = QWidget(self.tabs)
            new_chat.setLayout(grid)
            self.tabs.addTab(new_chat, f'Room - {title}')
        elif room_id == -1:
            QMessageBox.warning(
                self, "Warning", "This title is busy")
        else:
            QMessageBox.warning(
                self, "Warning", "This room doesn't exist")

    def init_ui(self):
        self.input = QTextEdit(self)
        self.input.setFont(QFont("Times", 16, QFont.Decorative))

        self.enter_btn = QPushButton('Send message', self)
        self.enter_btn.setFont(QFont("Times", 14, QFont.Decorative))
        self.enter_btn.clicked.connect(lambda i: self.send_usual_message(self.input))
        self.enter_btn.setShortcut('Enter')

        self.user_btn = QPushButton("User's list", self)
        self.user_btn.clicked.connect(self.list_of_users)

        self.quit_btn = QPushButton('Exit', self)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.add_room_btn = QPushButton('Create room', self)
        self.add_room_btn.clicked.connect(self.create_room)

        self.join_room_btn = QPushButton('Join room', self)
        self.join_room_btn.clicked.connect(self.join_room)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.input, 1, 0, 2, 4)
        grid.addWidget(self.enter_btn, 3, 1, 1, 2)
        grid.addWidget(self.user_btn, 4, 0)
        grid.addWidget(self.join_room_btn, 4, 1)
        grid.addWidget(self.add_room_btn, 4, 2)
        grid.addWidget(self.quit_btn, 4, 3)

        self.tabs = QTabWidget()
        self.common_chat = QWidget()
        self.tabs.addTab(self.common_chat, 'Common')
        self.common_chat.setLayout(grid)

        self.resize(800, 600)
        grid = QGridLayout()
        grid.addWidget(self.tabs, 1, 0, 4, 3)
        self.setLayout(grid)
        self.center()
        self.setWindowTitle(f'Chat - {self.nickname}')
        self.show()

    def upload_file(self, room):
        text, ok = QInputDialog.getText(self, 'Uploading of file',
                                        'Enter title of file from your room:')
        if ok:
            self.send_message(text, 8, room)

    def send_file(self, room):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/')[0]
        if fname:
            filesize = os.path.getsize(fname)
            self.send_message(fname.split('/')[-1], 7, room)
            self._socket.sendall(fname.split('/')[-1].encode() + b'\n')
            self._socket.sendall(str(filesize).encode() + b'\n')
            with open(fname, 'rb') as f:
                while True:
                    data = f.read(100000)
                    if not data:
                        break
                    self._socket.sendall(data)

    def make_message(self, message, status, room_id):
        return json.dumps({'from': self.nickname, 'message': message, 'status': status, 'room': room_id})

    def send_usual_message(self, input, room=0):
        message = input.toPlainText()
        input.clear()
        if message.strip():
            self.send_message(message, 3, room)

    def send_message(self, message, status, room=0):
        try:
            self._socket.send(self.make_message(message, status, room).encode('utf-8'))
        except ConnectionResetError:
            self.statusBar().showMessage('Server has gone away')

    def list_of_users(self, room_id=0):
        self.send_message(f'Users', 4, room_id)

    def look_files(self, room_id):
        self.send_message(f'Files', 9, room_id)

    def create_room(self):
        text, ok = QInputDialog.getText(self, 'Creating new room',
                                        'Enter room title:')
        if ok:
            self.send_message(f'New room_{text}_{0}', 5)

    def join_room(self):
        text, ok = QInputDialog.getText(self, 'Joining room',
                                        'Enter room title:')
        if ok:
            self.send_message(f'New room_{text}', 6)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def listen(self, sock):
        while True:
            try:
                data = sock.recv(1024).decode('utf-8')
                if not data:
                    continue
                data = json.loads(data)
                if data['status'] in [0, 2, 3]:
                    print(data['message'])
                elif data['status'] == 4:
                    print('-' * 22)
                    print('|', 'Users on channel'.center(20), '|', sep='')
                    print('-' * 22)
                    for i, user in enumerate(data['message']):
                        print('|', f'{i + 1}. {user}'.ljust(20), '|', sep='')
                    print('-' * 22)
                elif data['status'] == 5 and data['message'].startswith('ok'):
                    title = '_'.join(data['message'].split('_')[1:-1])
                    room_id = data['message'].split('_')[-1]

                    grid = QGridLayout()
                    grid.setSpacing(10)
                    input = QTextEdit(self)
                    input.setFont(QFont("Times", 16, QFont.Decorative))

                    enter_btn = QPushButton('Send message', self)
                    enter_btn.setFont(QFont("Times", 14, QFont.Decorative))
                    enter_btn.clicked.connect(lambda i: self.send_usual_message(input))
                    enter_btn.setShortcut('Enter')

                    user_btn = QPushButton("User's list", self)
                    user_btn.clicked.connect(lambda i: self.list_of_users(room_id))
                    #user_btn.clicked.connect(self.list_of_users)

                    quit_btn = QPushButton('Leave room', self)

                    grid.addWidget(input, 1, 0, 2, 4)
                    grid.addWidget(enter_btn, 3, 1, 1, 2)
                    grid.addWidget(user_btn, 4, 0)
                    grid.addWidget(quit_btn, 4, 3)

                    new_chat = QWidget(self.tabs)
                    new_chat.setLayout(grid)
                    self.tabs.addTab(new_chat, f'Room - {title}')

            except ConnectionResetError:
                break


app = QApplication(sys.argv)
connector = ConnectWindow()
sys.exit(app.exec_())
