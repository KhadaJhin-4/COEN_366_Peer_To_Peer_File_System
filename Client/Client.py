import socket
import sys
import threading
import re
import time

""" THE FOLLOWING TWO FUNCTIONS ARE CALLED BY UPDATE-INFO TO ENSURE THE USER IS NOT ENTERING A BAD IP OR SOCKET"""


# SUPPORT FUNCTION: function checks if the input string is a valid IPv4 address
def is_valid_ip(test_ip):
    try:
        socket.inet_aton(test_ip)  # Function in socket that ensures a ip address in the command line
        return True
    except (socket.error, OSError):  # both because the python version could affect this:
        return False


# SUPPORT FUNCTION: function checks if the input string is a valid UDP port number
def is_valid_udp_port(test_port):  # we are importing a helper to make it easy to check for invalid inputs
    return re.match(r'^[0-9]{1,5}$', test_port) is not None and 0 <= int(test_port) <= 65535


"""========================================================================================================"""


class Client:
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ip_addr = self.get_ip_address()
        self.udp_socket = self.set_udp(0)
        self.tcp_socket = self.set_tcp(0)
        self.registration_event = threading.Event()  # used to signal the end of an event in a thread to the main
        self.command_handlers = {  # commands are saved and linked with a dictionary for a clean call in the thread,
            "DE-REGISTER": self.Deregister,
            "PUBLISH": self.Publish,  # TODO: not implemented yet
            "REMOVE": self.Remove,  # TODO: not implemented yet
            "FILE-REQ": self.File_Request,
            "UPDATE-CONTACT": self.Update_info
        }

    # supporter function to assign the ip address dynamically
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
            threading.Thread(target=handler, args=(server_info,)).start()
        else:
            print("Unknown command (Client Side)")

    def Publish(self):
        print("Hi")

    def Remove(self):
        print("Hi")

    def File_Request(self):
        print("Hi")

    def Register(self, server_address):

        try:
            command = f"REGISTER {self.name} {self.ip_addr} {self.udp_socket}"
            self.udp_socket.sendto(command.encode(), server_address)

            # Waiting to receive a response from the server
            message, server = self.udp_socket.recvfrom(1024)
            print(f"{message.decode()}:{server}")
            if message.decode().split()[0] == "REGISTER-DENIED":
                print("Retry Registration")
                self.retry_registration()
            else:
                self.registration_event.set()  # communicates to the main to continue execution
        except socket.timeout:
            print("Server not responding. Timeout occurred.")

    # This serves as a helper function. it will only run inside of a current Register thread
    # if the user name already exists, this function ensures to get a different before the function
    # continues execution
    def retry_registration(self):
        new_name = input("Enter a different name: ")
        self.name = new_name.strip()
        server_address = (self.ip_addr, 3000)
        self.Register(server_address)

    def Deregister(self, server_address):
        try:
            command = f"DE-REGISTER {self.name}"
            self.udp_socket.sendto(command.encode(), server_address)  # send deregistration request

            #  waiting to receive a response from the server
            message, server = self.udp_socket.recvfrom(1024)
            print(f"{message.decode()}:{server}")
            message_received = message.decode().split()
            if message_received[0] == "DE-REGISTERED":
                self.udp_socket.close()
                self.name = ''
                self.ip_addr = ''
        except socket.timeout:
            print("Server not responding. Timeout occurred.")

    def Update_info(self, server_address):
        try:
            new_ip = input(f"Enter a new address or leave blank (Current IP {self.ip_addr}): ")
            # CONDITION TO CHECK IP VALIDITY
            if new_ip and not is_valid_ip(new_ip):
                print("Invalid IP address. Please enter a valid IPv4 address (eg. 192.168.1.100)")
                return
            if new_ip == '':
                new_ip = self.ip_addr  # no change to value
            new_udp = input(f"Enter a new socket or leave blank (Current socket {self.udp_socket.getsockname()[1]}): ")

            # CONDITION TO CHECK UDP VALIDITY
            if new_udp and not is_valid_udp_port(new_udp):
                print("Invalid UDP socket. Please enter a valid port number (0-65535).")
                return
            if new_udp == '':
                new_udp = self.udp_socket.getsockname()[1]  # no change
            # ========================================================================================================
            # ========================================================================================================
            command = f"UPDATE-CONTACT {self.name} {new_ip} {new_udp}"
            self.udp_socket.sendto(command.encode(), server_address)  # send update request

            #  waiting to receive a response from the server
            message, server = self.udp_socket.recvfrom(1024)
            print(f"{message.decode()}:{server}")
            message_received = message.decode().split()  # This receives back the response and makes the final change
            if message_received[0] == "UPDATE-CONFIRMED":
                self.udp_socket.close()  # Close the existing socket
                self.ip_addr = new_ip
                self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.udp_socket.bind((self.ip_addr, new_udp))
            self.registration_event.set()
        except socket.timeout:
            print("Server not responding. Timeout occurred.")


def main():
    # information registration, we just need the name by the user, the rest is defined inside the function
    name = input("Name the connection: ").strip()
    client = Client(name)
    server_address = (client.ip_addr, 3000)  # uses the current ip and the port to build the tuple
    threading.Thread(target=client.Register, args=(server_address,)).start()  # This is the first command by default since we are registering
    client.registration_event.wait()
    while True:
        command = input("Awaiting further requests: ")
        if command in client.command_handlers.keys():  # This is a way to make sure that the user has a valid input
            client.handle_command_server(command, server_address)
            client.registration_event.wait()
        else:
            print("Command doesnt exist, try a valid one")


if __name__ == "__main__":
    main()
