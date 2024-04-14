import socket
import threading
import time

port = 3000


class Server:
    def __init__(self):
        super().__init__()
        self.ip_addr = self.get_ip_address()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.ip_addr, port))
        self.list_registered = []
        self.lock = threading.Lock()
        self.command_handlers = {  # commands are saved and linked with a dictionary for a clean call in the thread
            "REGISTER": self.register_function,
            "DE-REGISTER": self.deregister_function,
            "PUBLISH": self.publish_function,  # TODO: not implemented yet
            "REMOVE": self.remove_function,  # TODO: not implemented yet
            "UPDATE-CONTACT": self.update_function
        }

    # same as client to dynamically assign the ip address
    def get_ip_address(self):  # This attempts to dynamically assign the ip address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip_address = s.getsockname()[0]
        except socket.error:
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address

    def register_function(self, client_address, parse_message):
        with self.lock:
            # FORMAT USED: command = f"REGISTER {self.name} {self.ip_addr} {self.udp_socket}"
            client_name = parse_message[1]  # we skip [0] because that's the command we already parsed
            ip_address = parse_message[2]
            udp_socket = parse_message[3]
            if client_name not in self.list_registered:
                self.list_registered.append(client_name)
                response = f"REGISTERED FIXED RQ FOR NOW"
                self.server_socket.sendto(response.encode(), client_address)
            else:
                response = f"REGISTER-DENIED RQ Name already exists in file"
                self.server_socket.sendto(response.encode(), client_address)

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

    def listen(self):
        print(f"Client listening on {self.ip_addr}:{port}")
        while True:
            request, client_address = self.server_socket.recvfrom(1024)  # constantly waiting for new messages
            parse_message = request.decode()  # turn to appropriate string first
            parse_message = parse_message.split()  # split into parts for easy parsing
            handler = self.command_handlers.get(
                parse_message[0])  # Receive the first input which has to be the command in a string format
            # This should map (similar to client) the command string with the appropriate function
            if handler:
                # Similar thread execution as before (in client)
                threading.Thread(target=handler, args=(client_address, parse_message)).start()
            else:
                print("Unknown Command (Server Side)")


def main():
    server = Server()
    server.listen()


if __name__ == "__main__":
    main()
