
from socket import *
import threading
import sys

class ChatServer(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.host = ''
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.clients = []
        self.running = True
        print(f"Chat server started on port {self.port}")

    def run(self):
        try:
            while self.running:
                client_socket, addr = self.server_socket.accept()
                self.clients.append(client_socket)
                print(f"Connection from {addr}")
                threading.Thread(target=self.client_thread, args=(client_socket, addr)).start()
        finally:
            for client in self.clients:
                client.close()
            self.server_socket.close()

    def client_thread(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"{addr}: {message}")
                    self.broadcast(message, client_socket)
                else:
                    break
            except Exception as e:
                print(f"Error from {addr}: {e}")
                break
        self.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"Error sending to a client: {e}")
                    self.remove(client)
                    client.close()

    def remove(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def stop_server(self):
        self.running = False
        new_sock = socket(AF_INET, SOCK_STREAM)
        new_sock.connect((self.host, self.port))
        new_sock.close()

if __name__ == "__main__":
    port = int(input("Enter port to host server on: "))
    server = ChatServer(port)
    server.start()
    try:
        input("Press enter to stop the server\n")
    finally:
        server.stop_server()
        server.join()
