
from socket import *
import threading
import sys

class ChatClient(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket(AF_INET, SOCK_STREAM)

    def run(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to chat server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Failed to connect to the server")
            return

        threading.Thread(target=self.receive, daemon=True).start()

        try:
            while True:
                message = input("")
                if message == ':q':
                    self.client_socket.send(message.encode())
                    break
                self.client_socket.send(message.encode())
        finally:
            self.client_socket.close()

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message == ':q':
                    break
                print(message)
            except:
                print("You have been disconnected from the server")
                break

if __name__ == "__main__":
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    client = ChatClient(host, port)
    client.start()
    client.join()
