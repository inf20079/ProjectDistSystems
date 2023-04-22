import json
import socket
import threading
from queue import Queue
from time import sleep

import select

from middleware.AbstractSocketListener import AbstractSocketListener
from middleware.types.MessageTypes import Coordinate


class BroadcastListener(AbstractSocketListener):

    def __init__(self, port: int):
        """ Instantiates BroadcastListener: listens on port for incoming broadcast messages.

        :param port: Port
        :type port: int
        """
        threading.Thread.__init__(self)
        self.port = port
        self.socket = self.configureSocket()
        self.client_threads = []
        self.message_queue = Queue()
        self.stop_event = threading.Event()

    def configureSocket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", self.port))
        return sock

    def run(self):
        while not self.stop_event.is_set():
            # Wait until there is data available to be read from the socket
            r_list, _, _ = select.select([self.socket], [], [], 0.1)

            # Read the data from the socket if available
            for sock in r_list:
                data, address = sock.recvfrom(1024)
                if not data:
                    continue
                message = json.loads(data.decode())
                message_parsed = self.parseMessage(message)
                self.message_queue.put(message_parsed)
        self.socket.close()


if __name__ == "__main__":
    sub = BroadcastListener(12003)
    sub.start()
    while True:
        print(sub.popMessage())
        sleep(0.2)
