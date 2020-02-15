import socket
import _thread
import json
import datetime


class Server:
    def __init__(self):
        self.connections = list()

    def make_message(self, message, status):
        return json.dumps({'message': message, 'status': status})

    def send_message(self, message):
        for conn in self.connections:
            conn[0].send(message.encode('utf-8'))

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
                            connection.send(self.make_message('no', 1).encode('utf-8'))
                            break
                    else:
                        connection.send(self.make_message('ok', 1).encode('utf-8'))
                elif data['status'] == 2:
                    now = datetime.datetime.now()
                    time = now.strftime("%H:%M:%S")
                    self.connections.append((connection, data['from']))
                    self.send_message(self.make_message(f'+ <{time}> {data["from"]} joined the chat', 2))
                elif data['status'] == 3:
                    self.send_message(self.make_message(f'[{data["from"]}]: {data["message"]}', 3))
                elif data['status'] == 4:
                    users = [conn[1] for conn in self.connections]
                    connection.send(self.make_message(users, 4).encode('utf-8'))
            except ConnectionResetError:
                message = ''
                i = 0
                now = datetime.datetime.now()
                time = now.strftime("%H:%M:%S")
                for i in range(len(self.connections)):
                    if self.connections[i][0] == connection:
                        message = f'- <{time}> {self.connections[i][1]} left the chat'
                        break
                self.connections.remove(self.connections[i])
                self.send_message(self.make_message(message, 0))
                connection.close()
                break
            except:
                pass


sock = socket.socket()
sock.bind(('', 9000))
sock.listen(10)
print("Started")
server = Server()
while True:
    conn, address = sock.accept()
    _thread.start_new_thread(server.on_new_client, (conn,))
