import socket


class Client:
    def __init__(self, sock: socket.socket,
                 username: str = None, password: str = None,
                 host: str = None, port: int = None):
        self.socket = sock
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.thread_ident = None

    # def set_thread_ident(self, thread_ident):
    #     self.thread_ident = thread_ident
    #
    # def get_thread_ident(self):
    #     return self.thread_ident
