class ClientData:

    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket, list_of_available_files, **_):
        self.TYPE = "CLIENT-DATA"
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket
        self.list_of_available_files = list_of_available_files

    def __str__(self):
        return """
        {self.TYPE}
        RQ#:\t{self.rq}
        Name:\t{self.name}
        IP address:\t{self.ip_address}
        UDP socket#:\t{self.udp_socket} 
        TCP socket#:\t{self.tcp_socket}
        List of avaliable files:\t{self.list_of_available_files}
        """
    def to_csv_row(self):
        return [self.rq, self.name, self.ip_address, self.udp_socket, self.tcp_socket, self.list_of_available_files]

    def set_modification(self, ip_address, udp_socket, tcp_socket, list_of_available_files):
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket
        self.list_of_available_files = list_of_available_files