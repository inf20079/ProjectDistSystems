import json
import socket
import threading
from queue import Queue

from middleware.types.MessageTypes import Coordinate


class BroadcastListener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", port))
        self.stop_event = threading.Event()
        self.message_queue = Queue()

    def run(self):
        while True:
            if self.stop_event.is_set():
                break
            data, address = self.sock.recvfrom(1024)
            if not data:
                break
            message = json.loads(data.decode())
            message_parsed = self.parseMessage(message)
            self.message_queue.put(message_parsed)
        self.sock.close()

    def popMessage(self):
        if self.message_queue.empty():
            return None
        else:
            return self.message_queue.get()

    @staticmethod
    def parseMessage(message):
        try:
            return Coordinate.fromDict(message)
        except TypeError:
            pass

    def shutdown(self):
        self.stop_event.set()

