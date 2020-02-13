import socket
import _thread
import json


class Server:
    def __init__(self):
        self.connections = list()

    def send_message(self, message):
        for conn in self.connections:
            conn[0].send(message.encode('utf-8'))

    def on_new_client(self, connection, addr):
        while True:
            try:
                data = json.loads(connection.recv(1024).decode('utf-8'))
                if not data:
                    continue
                if data['status'] == 2:
                    self.send_message(f'[{data["from"]}]: {data["message"]}')
                elif data['status'] == 1:
                    self.connections.append((connection, data['from']))
                    self.send_message(f'+ {data["from"]} joined the chat')
            except ConnectionResetError:
                message = ''
                for i in range(len(self.connections)):
                    if self.connections[i][0] == connection:
                        message = f'- {self.connections[i][1]} left the chat'
                        break
                self.connections.remove(self.connections[i])
                self.send_message(message)
                connection.close()
                break


sock = socket.socket()
sock.bind(('', 9000))
sock.listen(10)
print("Started")
server = Server()
while True:
    connection, address = sock.accept()
    _thread.start_new_thread(server.on_new_client, (connection, address))
