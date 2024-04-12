class Register:

    def __init__(self, rq, name, ip_address, udp_socket, **_):
        self.TYPE = "REGISTER"
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


class Registered:

    def __init__(self, rq, **_):
        self.TYPE = "REGISTERED"
        self.rq = rq

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq} 
        """


class RegisterDenied:

    def __init__(self, rq, reason, **_):
        self.TYPE = "REGISTER-DENIED"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        Reason:\t{self.reason}
        """


class DeRegister:

    def __init__(self, rq, name, **_):
        self.TYPE = "DE-REGISTER"
        self.rq = rq
        self.name = name

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        Name:\t{self.name}
        """
