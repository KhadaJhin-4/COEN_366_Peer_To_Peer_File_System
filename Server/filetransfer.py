class FileReq:

    def __init__(self, rq, file_name, **_):
        self.TYPE = "FILE-REQ"
        self.rq = rq
        self.file_name = file_name

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        File-name:\t{self.file_name}
        """

class FileConf:

    def __init__(self, rq, tcp_socket, **_):
        self.TYPE = "FILE-CONF"
        self.rq = rq
        self.tcp_socket = tcp_socket

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        TCP socket#:\t{self.tcp_socket}
        """

class File:

    def __init__(self, rq, file_name, chunk, text, **_):
        self.TYPE = "FILE"
        self.rq = rq
        self.file_name = file_name
        self.chunk = chunk
        self.text = text

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        File-name:\t{self.file_name}
        Chunk#:\t{self.chunk}
        Text:\t{self.text}
        """

class FileEnd:

    def __init__(self, rq, file_name, chunk, text, **_):
        self.TYPE = "FILE-END"
        self.rq = rq
        self.file_name = file_name
        self.chunk = chunk
        self.text = text

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        File-name:\t{self.file_name}
        Chunk#:\t{self.chunk}
        Text:\t{self.text}
        """

class FileError:

    def __init__(self, rq, reason, **_):
        self.TYPE = "FILE-ERROR"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
        {self.TYPE}
        RQ#:\t{self.rq}
        Reason:\t{self.reason}
        """