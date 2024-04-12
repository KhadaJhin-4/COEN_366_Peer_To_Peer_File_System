import socket
import threading
import time
import json

host = 'localhost'
port = 3000


class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.list_registered = []
        self.lock = threading.Lock()
        self.command_handlers = {  # commands are saved and linked with a dictionary for a clean call in the thread
            "REGISTER": self.register_function,
            "DE-REGISTER": self.deregister_function,
            "PUBLISH": self.publish_function,  # TODO: not implemented yet
            "REMOVE": self.remove_function,  # TODO: not implemented yet
            "UPDATE-CONTACT": self.update_function
        }

    def register_function(self, client_info, client_address):
        with self.lock:
            client_name = client_info.get('name')
            if client_name not in self.list_registered:
                self.list_registered.append(client_name)
                response = "Client was added to the Server!"
                self.server_socket.sendto(response.encode(), client.ip_addr)
            else:
                response = "Name already exists in list"
                self.server_socket.sendto(response.encode(), client.ip_addr)

    def deregister_function(self, client):
        with self.lock:
            if client.name in self.list_registered:
                self.list_registered.remove(client)
                response = "DE-REGISTERED: "
                self.server_socket.sendto(response.encode(), client.ip_addr)

    def update_function(self):
        print("Hi")

    def publish_function(self):
        print("HI")

    def remove_function(self):
        print("HI")

    def run(self):
        print(f"Server is listening on {host}:{port}")

        while True:
            time.sleep(1)
            data, client_address = self.server_socket.recvfrom(1024)
            message = data.decode().strip()
            # let's split the info to parse it:
            try:
                client_info = json.loads(message)

                handler = self.command_handlers.get(  # parts[0] is meant to be the command from the request message
                    parts[0])  # This is called to check if the command sent is correct and exists in the system
            if handler:
                handler(client_address)
            else:
                response = "Unknown Command"
                self.server_socket.sendto(response.encode(), client.ip_addr)


def main():
    server = Server()
    server.daemon = True
    server.start()

    # Block the main thread indefinitely
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        server.join()


if __name__ == "__main__":
    main()
