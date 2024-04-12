import socket

def udp_client():
    host = 'localhost'   # The server's hostname or IP address
    port = 12345         # The port used by the server

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send data
    message = 'Hello, server!'
    client_socket.sendto(message.encode(), (host, port))

    # Receive data from the server
    data, server = client_socket.recvfrom(1024)
    print('Received:', data.decode())

    # Close the socket
    client_socket.close()


udp_client()
