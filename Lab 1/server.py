import socket
import _thread
import json
import datetime
import os
import time


class Room:
    def __init__(self, title, connection, max_num):
        self.title = title
        self.connections = [connection]
        self.max_num = max_num

    def join_room(self, connection):
        if len(self.connections) < self.max_num:
            self.connections.append(connection)
            return True
        else:
            return False


class Server:
    def __init__(self):
        self.connections = list()
        self.rooms = list()
        for file in os.listdir('files'):
            os.remove(os.path.join('files', file))

    def make_message(self, message, status, room):
        return json.dumps({'message': message, 'status': status, 'room': room})

    def send_message(self, message, status, room=0):
        if room == 0:
            for conn in self.connections:
                conn[0].send(self.make_message(message, status, room).encode('utf-8'))
        else:
            users = [conn[0] for conn in self.rooms[room-1].connections]
            for conn in self.rooms[room-1].connections:
                conn[0].send(self.make_message(message, status, room).encode('utf-8'))

    def on_new_client(self, connection):
        while True:
            try:
                data = connection.recv(1024).decode('utf-8')
                if not data:
                    continue
                data = json.loads(data)
                if data['status'] == 1:
                    for conn in self.connections:
                        if conn[1] == data['from']:
                            connection.send(self.make_message('no', 1, 0).encode('utf-8'))
                            break
                    else:
                        connection.send(self.make_message('ok', 1, 0).encode('utf-8'))
                elif data['status'] == 2:
                    now = datetime.datetime.now()
                    time = now.strftime("%H:%M:%S")
                    self.connections.append((connection, data['from']))
                    self.send_message(f'+ <{time}> {data["from"]} joined the chat', 2)
                elif data['status'] == 3:
                    if data['room']:
                        room_title = self.rooms[data['room'] - 1].title
                        self.send_message(f'{room_title}>[{data["from"]}]: {data["message"]}', 3, data['room'])
                    else:
                        self.send_message(f'Common>[{data["from"]}]: {data["message"]}', 3)
                elif data['status'] == 4:
                    if data['room'] != 0:
                        users = [conn[1] for conn in self.rooms[data['room']-1].connections]
                        connection.send(self.make_message(users, 4, data['room']).encode('utf-8'))
                    else:
                        users = [conn[1] for conn in self.connections]
                        connection.send(self.make_message(users, 4, 0).encode('utf-8'))
                elif data['status'] == 5:
                    title = '_'.join(data['message'].split('_')[1:-1])
                    num = int(data['message'].split('_')[-1])
                    for room in self.rooms:
                        if room.title == title:
                            connection.send(self.make_message('no', 5, 0).encode('utf-8'))
                            break
                    else:
                        new_room = Room(title, (connection, data['from']), num)
                        self.rooms.append(new_room)
                        connection.send(self.make_message(f'ok_{title}_{len(self.rooms)}', 5, 0).encode('utf-8'))
                elif data['status'] == 6:
                    title = '_'.join(data['message'].split('_')[1:])
                    for i in range(len(self.rooms)):
                        if self.rooms[i].title == title:
                            self.rooms[i].connections.append((connection, data['from']))
                            connection.send(self.make_message(f'ok_{title}_{i+1}', 6, 0).encode('utf-8'))
                            break
                    else:
                        connection.send(self.make_message(f'no', 6, 0).encode('utf-8'))
                elif data['status'] == 7:
                    filename = data['message']
                    with connection.makefile('rb') as file:
                        while True:
                            raw = file.readline()
                            if not raw:
                                break
                            filename = f'room{data["room"]}_{raw.strip().decode()}'
                            length = int(file.readline())
                            path = os.path.join('files', filename)
                            with open(path, 'wb') as f:
                                while length:
                                    data = file.read(min(length, 100000))
                                    if not data:
                                        break
                                    f.write(data)
                                    length -= len(data)
                            print(f'-- File was uploaded to files/{filename} --')
                            connection.send(self.make_message(f'File was uploaded', 7, 0).encode('utf-8'))
                            break
                    _thread.start_new_thread(delete_file, (os.path.join('files', filename), 60))
                elif data['status'] == 8:
                    file = f'room{data["room"]}_{data["message"]}'
                    if file in os.listdir('files'):
                        fname = os.path.join('files', file)
                        filesize = os.path.getsize(fname)
                        connection.send(self.make_message(data["message"], 8, 0).encode('utf-8'))
                        connection.sendall(fname.split('\\')[-1].encode() + b'\n')
                        connection.sendall(str(filesize).encode() + b'\n')
                        with open(fname, 'rb') as f:
                            while True:
                                data = f.read(100000)
                                if not data:
                                    break
                                connection.sendall(data)
                    else:
                        connection.send(self.make_message('no', 80, 0).encode('utf-8'))
                elif data['status'] == 9:
                    all_files = os.listdir('files')
                    files = [file.split('_')[1] for file in all_files if file.startswith(f'room{data["room"]}')]
                    room_title = self.rooms[data['room'] - 1].title
                    connection.send(self.make_message('|'.join(files), 9, room_title).encode('utf-8'))
            except (ConnectionResetError, ConnectionAbortedError):
                message = ''
                i = 0
                now = datetime.datetime.now()
                time = now.strftime("%H:%M:%S")
                for i in range(len(self.connections)):
                    if self.connections[i][0] == connection:
                        message = f'- <{time}> {self.connections[i][1]} left the chat'
                        break
                self.connections.remove(self.connections[i])
                self.send_message(message, 0, 0)
                connection.close()
                break
            # except Exception as e:
            #     print(e)


def delete_file(path, delay=100):
    time.sleep(delay)
    os.remove(path)

sock = socket.socket()
sock.bind(('', 9000))
sock.listen(10)
print("Started")
server = Server()
while True:
    conn, address = sock.accept()
    _thread.start_new_thread(server.on_new_client, (conn,))
