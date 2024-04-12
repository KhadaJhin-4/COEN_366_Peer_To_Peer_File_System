class UpdateContact:

    def __init__(self, rq, name, ip_address, udp_socket, **_):
        self.TYPE = "UPDATE-CONTACT"
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        Name:\t{self.name}
        IP Address:\t{self.ip_address}
        UDP socket#:\t{self.udp_socket} 
        """


class UpdateConfirmed:

    def __init__(self, rq, name, ip_address, udp_socket, **_):
        self.TYPE = "UPDATE-CONFIRMED"
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        Name:\t{self.name}
        IP Address:\t{self.ip_address}
        UDP socket#:\t{self.udp_socket} 
        """


class UpdateDenied:

    def __init__(self, rq, name, reason, **_):
        self.TYPE = "UPDATE-DENIED"
        self.rq = rq
        self.name = name
        self.reason = reason

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        Name:\t{self.name}
        Reason:\t{self.reason}
        """
