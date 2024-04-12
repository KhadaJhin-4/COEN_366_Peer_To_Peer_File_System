import socket
import threading


class Client(threading.Thread):
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
            "UPDATE-CONTACT": self.Update,
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

    def set_udp(self, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.ip_addr, port))
        udp_socket.settimeout(3)
        return udp_socket

    def set_tcp(self, port):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((self.ip_addr, port))
        return tcp_socket

    def Publish(self):
        print("Hi")

    def Remove(self):
        print("Hi")

    def Update(self):
        print("Hi")

    def File_Request(self):
        print("Hi")

    def Register(self, server_address):
        client_info = { #we send this dictionary with all the info to make it easier to parse on the server side
            'name': self.name,
            'ip_address': self.ip_addr,
            'udp_socket': self.udp_socket
        }
        command = f"REGISTER {client_info}"
        self.udp_socket.sendto(command.encode(), server_address)

    def Deregister(self, server_address):
        command = f"DE-REGISTER {self.name}"
        self.udp_socket.sendto(command.encode(), server_address)
        print(f"DE-REGISTER {self.name}")

    def run(self):
        print("Client is initialized")
        server_address = (self.ip_addr, 3000)  # uses the current ip and the port to build the tuple
        self.Register(server_address)

        while True:
            command = input("Awaiting further commands:")
            if command == "DE-REGISTER":
                self.Deregister(server_address)
            else:
                print("invalid command")


def main():
    # information registration, we just need the name by the user, the rest is defined inside the function
    name = input("Name the connection: ").strip()
    client = Client(name)
    client.start()


if __name__ == "__main__":
    main()
