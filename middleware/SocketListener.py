import socket
import json
import threading
from queue import Queue
from time import sleep

import select

from middleware.types.MessageTypes import Coordinate


class SocketListener(threading.Thread):
    def __init__(self, host: str, port: int):
        """ Instantiates SocketListener: listens on port for incoming messages.

        :param host: IPv4 Adress
        :type host: str
        :param port: Port
        :type port: int
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.client_threads = []
        self.message_queue = Queue()
        self.stop_event = threading.Event()

    def run(self):
        while True:
            if self.stop_event.is_set():
                break
            client_socket, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.listenToClient, args=(client_socket,))
            client_thread.start()
            self.client_threads.append(client_thread)

    def listenToClient(self, client_socket):
        while True:
            if self.stop_event.is_set():
                break
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            message_parsed = self.parseMessage(message)
            self.message_queue.put(message_parsed)
        client_socket.close()

    def popMessage(self):
        if self.message_queue.empty():
            return None
        else:
            return self.message_queue.get()

    def shutdown(self):
        self.socket.close()
        self.stop_event.set()

    @staticmethod
    def parseMessage(message):
        try:
            return Coordinate.fromDict(message)
        except TypeError:
            pass


if __name__ == "__main__":
    sub = SocketListener("localhost", 12001)
    sub.start()
    while True:
        print(sub.popMessage())
        sleep(0.2)
