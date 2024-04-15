import socket
import json

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
server_address = ('0.0.0.0', 12345)
server_socket.bind(server_address)

# Function to determine local IP address
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        return ip
    except Exception:
        return "Unable to determine local IP"

local_ip = get_local_ip()
print(f'Server is listening on IP {local_ip}...')

# Function to handle registering clients
def register_client(client_name, client_address):
    try:
        with open('clients.json', 'r+') as file:
            data = json.load(file)
            if client_name in data:
                return "Registration failed: Name already exists."
            # Register new client
            data[client_name] = {"ip": client_address[0]}
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return "Client registered successfully."
    except json.JSONDecodeError:
        return "Error reading JSON file."
    except FileNotFoundError:
        with open('clients.json', 'w') as file:
            json.dump({client_name: {"ip": client_address[0]}}, file, indent=4)
        return "Client registered and file created."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to deregister a client
def deregister_client(client_name):
    try:
        with open('clients.json', 'r+') as file:
            data = json.load(file)
            if client_name in data:
                del data[client_name]  # Remove the client entry
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                return "Client deregistered successfully."
            else:
                return "No action taken: Client not registered."
    except json.JSONDecodeError:
        return "Error reading JSON file."
    except FileNotFoundError:
        return "No action taken: Client list file not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

while True:
    # Receive command from client and client address
    data, client_address = server_socket.recvfrom(1024)
    command, _, client_name = data.decode().partition(':')

    if command.strip().lower() == "register":
        response = register_client(client_name, client_address)
        server_socket.sendto(response.encode(), client_address)
    elif command.strip().lower() == "deregister":
        response = deregister_client(client_name)
    elif command.strip().lower() == "exit":
        response = "Client exiting."
        server_socket.sendto(response.encode(), client_address)
    else:
        response = "Unknown command or message."
        server_socket.sendto(response.encode(), client_address)
