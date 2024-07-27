from socket import *
import threading

class ChatServer(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.host = ''
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.clients = {}
        self.client_id = 1
        print(f"Chat server started on port {self.port}")

    def run(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                client_label = f"Client {self.client_id}"
                self.clients[client_socket] = client_label
                print(f"Connection from {addr}, assigned as {client_label}")
                threading.Thread(target=self.client_thread, args=(client_socket, client_label)).start()
                self.client_id += 1
        finally:
            for client in self.clients:
                client.close()
            self.server_socket.close()

    def client_thread(self, client_socket, client_label):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Received from {client_label}: {message}")
                    self.broadcast(message, client_socket, client_label)
                else:
                    break
            except Exception as e:
                print(f"Error from {client_label}: {e}")
                break
        self.remove(client_socket)
        client_socket.close()

    def broadcast(self, message, client_socket, sender_label):
        for client, label in self.clients.items():
            if client != client_socket:
                try:
                    client.send(f"{sender_label}: {message}".encode())
                except Exception as e:
                    print(f"Error sending to {label}: {e}")
                    self.remove(client)
                    client.close()

    def remove(self, client):
        if client in self.clients:
            del self.clients[client]

    def stop_server(self):
        for client in list(self.clients):
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    port = int(input("Enter port to host server on: "))
    server = ChatServer(port)
    server.start()
    try:
        input("Press enter to stop the server\n")
    finally:
        server.stop_server()
        server.join()
