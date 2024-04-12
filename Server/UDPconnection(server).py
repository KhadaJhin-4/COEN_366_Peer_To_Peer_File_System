import socket

def udp_server():
    host = 'localhost'   # Host address
    port = 12345         # Port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the host and port
    server_socket.bind((host, port))
    print('UDP Server is listening on {}:{}'.format(host, port))

    # Receive data from the client
    while True:
        data, addr = server_socket.recvfrom(1024)
        print('Received from {}: {}'.format(addr, data.decode()))

        # Send data back as an echo
        server_socket.sendto(data, addr)

udp_server()
