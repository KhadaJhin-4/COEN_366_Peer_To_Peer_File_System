import socket

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Request server address and port from user
server_ip = input("Enter server IP address: ")
server_port = int(input("Enter server port number: "))
server_address = (server_ip, server_port)

# Set timeout for the client socket (in seconds)
client_socket.settimeout(5)  # 5 seconds timeout

while True:
    try:
        # Read command from user
        command = input("Enter command (register/deregister/exit) or message to send to server: ")

        # Construct message with command and client name if needed
        if command.lower() in ["register", "deregister"]:
            client_name = input("Enter your client name: ")
            full_command = f"{command}:{client_name}"
        else:
            full_command = command

        # Send command to server
        client_socket.sendto(full_command.encode(), server_address)

        if command.lower() == "exit":
            print("Exiting client.")
            break

        # Receive response from server
        data, server = client_socket.recvfrom(1024)
        print(f"Received response from {server}: {data.decode()}")

    except socket.timeout:
        print("Server not responding. Timeout occurred.")
        break

# Close the socket
client_socket.close()
