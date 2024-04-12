class Update:

    def __init__(self, name, ip_address, udp_socket, list_of_available_files, **_):
        self.TYPE = "UPDATE"
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.list_of_available_files = list_of_available_files

    def __str__(self):
        return f"""
        {self.TYPE}
        Name:\t{self.name}
        IP address:\t{self.ip_address}
        UDP socket#:\t{self.udp_socket} 
        List of available files:\t{self.list_of_available_files}
        """