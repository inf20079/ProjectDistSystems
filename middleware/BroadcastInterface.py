import json
import socket
import threading
from queue import Queue
from time import sleep
from typing import Any

import select

from middleware.AbstractSocketListener import AbstractSocketListener
from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate


class BroadcastInterface(AbstractSocketListener):

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
        self.publish_queue = Queue()
        self.stop_event = threading.Event()

    def configureSocket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", self.port))
        return sock

    def run(self):
        while True:
            if self.stop_event.is_set(): break
            # Wait until there is data available to be read from the socket
            try:
                r_list, w_list, _ = select.select([self.socket], [self.socket], [], 0.1)
            except ValueError:
                break
            except OSError:
                break

            # Read the data from the socket if available
            if r_list:
                try:
                    data, address = self.socket.recvfrom(1024)
                except OSError:
                    break
                if not data:
                    continue
                message = json.loads(data.decode())
                message_parsed = self.parseMessage(message)
                self.message_queue.put(message_parsed)

            if w_list:
                if not self.publish_queue.empty():
                    message = self.publish_queue.get()
                    message_json_string = json.dumps(message, cls=EnhancedJSONEncoder)
                    try:
                        self.socket.sendto(message_json_string.encode(), ("<broadcast>", self.port))
                    except OSError:
                        break

        self.socket.close()

    def appendMessage(self, message: Any):
        self.publish_queue.put(message)

    def __del__(self):
        self.socket.close()


if __name__ == "__main__":
    sub = BroadcastInterface(12003)
    sub.start()
    i = 0
    while i <= 5:
        i += 1
        sub.appendMessage(Coordinate(i, 2))
        print(sub.publish_queue.queue)
        sleep(0.5)
        print(sub.popMessage())

    sub.shutdown()
    sub.join()
