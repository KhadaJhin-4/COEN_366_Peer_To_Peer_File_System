import socket
import threading
import time

port = 3000


# This class captures the essential elements of a client so that we can facilitate communication with other clients
class Client:
    def __init__(self, name, ip, udp):
        self.name = name
        self.ip = ip
        self.udp = udp
        # TODO: will probably need space for the files too


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
            "UPDATE-CONTACT": self.update_info_function
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
            client = Client(client_name, ip_address, udp_socket)
            if client_name not in self.list_registered:
                self.list_registered.append(client)
                response = f"REGISTERED FIXED RQ FOR NOW"
                self.server_socket.sendto(response.encode(), client_address)
            else:
                response = f"REGISTER-DENIED RQ Name already exists in file"
                self.server_socket.sendto(response.encode(), client_address)

    def deregister_function(self, client_address, parse_message):
        with self.lock:
            # FORMAT USED: command = f"DE-REGISTER {self.name}"
            client_name = parse_message[1]  # TODO:the info passed is the command and the name for now

            # Check if any object in list_registered has the given client name
            matching_client = [client for client in self.list_registered if client.name == client_name]

            # here we are simply checking if the name given exists in the list of objects of a client
            if matching_client:
                client = matching_client[0]  # we pass the client into a variable for clarity
                self.list_registered.remove(client)
                response = f"DE-REGISTERED: {client_name}"
                self.server_socket.sendto(response.encode(), client_address)
            # no else condition is defined since the server doesn't care about a client not existing

    def update_info_function(self, client_address, parse_message):
        with self.lock:
            # FORMAT USED: command = f"UPDATE-CONTACT {self.name} {new_ip} {new_udp}"
            client_name = parse_message[1]
            new_ip = parse_message[2]  # we have ensured that new_ip and new_udp are either unchanged or new in client
            new_udp = parse_message[3]

            # Check if any object in list_registered already has the given IP we added
            matching_socket = [client for client in self.list_registered if client.udp == new_udp]
            # Separated for clarity------------------------------------------------------------------------
            # Check if any object in list_registered already has the given socket we added
            matching_ip = [client for client in self.list_registered if client.ip == new_ip]

            reason = ''  # this is the reason that will be fed on the output, it will change based on ip and socket
            # status
            if matching_ip:
                reason += "IP value is already in use. "
            if matching_socket:
                reason += "Socket is already in use. "
            if matching_socket or matching_ip:
                response = f"UPDATE-DENIED RQ {client_name} {reason}"
                self.server_socket.sendto(response.encode(), client_address)
            else:
                # Just a loop to find the client and pass the new info
                matching_client = [client for client in self.list_registered if client.name == client_name]
                if not matching_client:
                    reason = "Name was not found in server"
                    response = response = f"UPDATE-DENIED RQ {client_name} {reason}"
                    self.server_socket.sendto(response.encode(), client_address)
                else:
                    # Update the client's information
                    client = matching_client[0]  # extract the client
                    client.ip_addr = new_ip
                    client.udp_socket = new_udp
                    response = f"UPDATE-CONFIRMED RQ {client_name} {new_ip} {new_udp}"
                    self.server_socket.sendto(response.encode(), client_address)

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
