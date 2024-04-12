import socket

def tcp_server():
    host = 'localhost'   # Host address
    port = 12345         # Port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print('TCP Server is listening on {}:{}'.format(host, port))

    # Accept a connection
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)

    # Receive data from the client
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print('Received:', data.decode())

        # Send data back as an echo
        client_socket.sendall(data)

    # Close the connection
    client_socket.close()

tcp_server()
