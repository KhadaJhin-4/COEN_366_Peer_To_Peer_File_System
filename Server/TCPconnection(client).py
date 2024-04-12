import socket


def tcp_client():
    host = 'localhost'  # The server's hostname or IP address
    port = 12345  # The port used by the server

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print('Connected to {}:{}'.format(host, port))

    # Send data
    message = 'Hello, server!'
    client_socket.sendall(message.encode())

    # Receive data from the server
    data = client_socket.recv(1024)
    print('Received:', data.decode())

    # Close the connection
    client_socket.close()


tcp_client()
