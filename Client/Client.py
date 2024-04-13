import socket
import threading


class Client:
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ip_addr = self.get_ip_address()
        self.udp_socket = self.set_udp(0)
        self.tcp_socket = self.set_tcp(0)
        self.command_handlers = {  # commands are saved and linked with a dictionary for a clean call in the thread,
            "DE-REGISTER": self.Deregister,
            "PUBLISH": self.Publish,  # TODO: not implemented yet
            "REMOVE": self.Remove,  # TODO: not implemented yet
            "FILE-REQ": self.File_Request,
            "UPDATE-CONTACT": self.Update
        }

    # supporter function to assign the ip address
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

    # more helper functions to initialize UDP and TCP
    def set_udp(self, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.ip_addr, port))
        return udp_socket

    def set_tcp(self, port):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((self.ip_addr, port))
        return tcp_socket

    # This function receives a command in a string and links the dictionary to the appropriate command
    # Then, it starts a thread to deal with the command
    def handle_command_server(self, command, server_info):
        handler = self.command_handlers.get(command)
        if handler:
            # Start a new thread to execute the handler function
            threading.Thread(target=handler).start()
        else:
            print("Unknown command")

    def Publish(self):
        print("Hi")

    def Remove(self):
        print("Hi")

    def Update(self):
        print("Hi")

    def File_Request(self):
        print("Hi")

    def Register(self, server_address):
        try:
            client_info = {  # we send this dictionary with all the info to make it easier to parse on the server side
                'name': self.name,
                'ip_address': self.ip_addr,
                'udp_socket': self.udp_socket
            }
            command = f"REGISTER {client_info}"
            self.udp_socket.sendto(command.encode(), server_address)

            # Waiting to receive a response from the server
            message, server = self.udp_socket.recvfrom(1024)
            print(f"{message.decode()}:{server}")
        except socket.timeout:
            print("Server not responding. Timeout occurred.")

    def Deregister(self, server_address):
        command = f"DE-REGISTER {self.name}"
        self.udp_socket.sendto(command.encode(), server_address)
        print(f"DE-REGISTER {self.name}")


def main():
    # information registration, we just need the name by the user, the rest is defined inside the function
    name = input("Name the connection: ").strip()
    client = Client(name)
    server_address = (client.ip_addr, 3000)  # uses the current ip and the port to build the tuple
    client.handle_command_server("REGISTER", server_address)  # This is the first command by default since we are registering
    while True:
        command = input("Awaiting further requests: ")
        if command in client.command_handlers.keys():  # This is a way to make sure that the user has a valid input
            client.handle_command_server(command, server_address)
        else:
            print("Command doesnt exist, try a valid one")


if __name__ == "__main__":
    main()
