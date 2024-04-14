import socket
import threading
import time
import json

host = 'localhost'
port = 3000

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.clients = {}  # Updated to use a dictionary for clients
        self.lock = threading.Lock()
        self.command_handlers = {
            "REGISTER": self.register_function,
            "DE-REGISTER": self.deregister_function,
            "PUBLISH": self.publish_function,
            "REMOVE": self.remove_function,
            "UPDATE-CONTACT": self.update_function
        }

    def register_function(self, client_info, client_address):
        with self.lock:
            client_name = client_info.get('name')
            if client_name not in self.clients:
                self.clients[client_name] = {
                    "address": client_address,
                    "files": []
                }
                response = "Client was added to the Server!"
                self.server_socket.sendto(response.encode(), client_address)
            else:
                response = "Name already exists in list"
                self.server_socket.sendto(response.encode(), client_address)
            self.update_function()

    def deregister_function(self, client_info, client_address):
        client_name = client_info.get('name')
        with self.lock:
            if client_name in self.clients:
                del self.clients[client_name]
                response = "DE-REGISTERED: " + client_name
                self.server_socket.sendto(response.encode(), client_address)
            else:
                response = "Client was not found"
                self.server_socket.sendto(response.encode(), client_address)
            self.update_function()

    def update_function(self):
        with self.lock:
            update_list = [
                {
                    "name": name,
                    "address": client["address"][0],
                    "port": client["address"][1],
                    "files": client["files"]
                } for name, client in self.clients.items()
            ]
            update_message = json.dumps({"command": "UPDATE", "data": update_list})
            for client in self.clients.values():
                self.server_socket.sendto(update_message.encode(), client["address"])

    def listen_for_requests(self):
        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            message = data.decode().strip()
            try:
                client_info = json.loads(message)
                command = client_info.get("command")
                handler = self.command_handlers.get(command)
                if handler:
                    # Instead of handling directly, we just return the data needed for processing
                    return handler, client_info, client_address
            except Exception as e:
                print(f"Failed to process message: {e}")

def handle_client_request(server, handler, client_info, client_address):
    handler(client_info, client_address)

def main():
    server = Server()

    try:
        while True:
            result = server.listen_for_requests()
            if result:
                handler, client_info, client_address = result
                client_thread = threading.Thread(target=handle_client_request, args=(server, handler, client_info, client_address))
                client_thread.start()
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
