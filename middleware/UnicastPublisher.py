import socket
import json
import threading
from queue import Queue
from time import sleep
from typing import Type, TypeVar, List
from dataclasses import dataclass, asdict

from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate


class UnicastPublisher(threading.Thread):
    def __init__(self, host: str, port: int):
        """ Class which makes unicast to a list of sockets possible. To add a socket use registerListener. If you want to send a message to all the listeners
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.message_queue = Queue()
        self.stop_event = threading.Event()
        self.timeoutevents = 0

    def appendMessage(self, message):
        """Append a message to the queue."""
        self.message_queue.put(message)

    def run(self):
        """Start listening to incoming connections and publishing messages to listeners."""
        while True:
            if self.stop_event.is_set():
                break
            if not self.message_queue.empty():
                message = self.message_queue.get()

                try:
                    message_json = json.dumps(message, cls=EnhancedJSONEncoder).encode()
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.host, self.port))
                        s.sendall(message_json)
                except ConnectionRefusedError:
                    print("Failed to establish connection trying again in 0.5s  (ConnectionRefusedError)")
                    sleep(0.5)
                    self.timeoutevents += 1
            if self.timeoutevents >= 5:
                raise ConnectionRefusedError("Failed to establish connection 5 times. Host not reachable.")

    def shutdown(self):
        self.stop_event.set()


if __name__ == "__main__":
    pub = UnicastPublisher("localhost", 12004)
    pub.start()

    i = 0
    while True:
        i += 1
        pub.appendMessage(Coordinate(i, 3))
        sleep(0.2)
        print(i)