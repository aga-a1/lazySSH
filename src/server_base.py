import socket
import threading
from src.logging import logger
import time

from abc import ABC, abstractmethod
from sys import platform

from src.client import Client

import logging



class ServerBase(ABC):
    def __init__(self):
        # create a multithreaded event, which is basically a
        # thread-safe boolean
        self._is_running = threading.Event()

        # this socket will be used to listen to incoming connections
        self._socket = None

        # this will contain the shell for the connected client.
        # we don't yet initialize it, since we need to get the
        # stdin and stdout objects after the connection is made.
        self.client_shell = None

        # this will contain the thread that will listen for incoming
        # connections and data.
        self._listen_thread = None

        self.client_thread = None

    # To start the server, we open the socket and create
    # the listening thread.
    def start(self, address='127.0.0.1', port=22, timeout=1):
        if not self._is_running.is_set():
            self._is_running.set()

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

            # reuse port is not avaible on windows
            if platform == "linux" or platform == "linux2":
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, True)

            self._socket.settimeout(timeout)
            self._socket.bind((address, port))

            self._listen_thread = threading.Thread(target=self._listen, name='Thread-Listener', daemon=True)
            self._listen_thread.start()
            # self._listen_thread.join()
            if self._listen_thread.is_alive():
                logger.info('Listener has been started')


    # To stop the server, we must join the listen thread
    # and close the socket.
    def stop(self):
        if self._is_running.is_set():
            self._is_running.clear()
            self._listen_thread.join()
            self._socket.close()

    # The listen function will constantly run if the server is running.
    # We wait for a connection, if a connection is made, we will call
    # our connection function.
    def _listen(self):
        while self._is_running.is_set():
            try:
                # logger.info("listening")
                self._socket.listen()
                c_socket, addr = self._socket.accept()  # is blocking until a new connection comes in
                logger.debug('new client tries to connect from ' + str(addr[0]) + ':' + str(addr[1]))
                client = Client(c_socket, host=addr[0], port=addr[1])

                # htop -p 184067, F2 - Display Options - Show custom Threads
                self.client_thread = threading.Thread(target=self.connection_function, args=(client,), daemon=True)
                self.client_thread.start()
                # self.client_thread.
            except Exception as error:
                print("xxx An exception occurred:", error)

    @abstractmethod
    def connection_function(self, client: Client):
        pass

