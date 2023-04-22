import socket
import json
import threading
from queue import Queue
from time import sleep
from typing import Type, TypeVar, List
from dataclasses import dataclass, asdict

from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate

T = TypeVar("T")


@dataclass
class Listener:
    host: str
    port: int


class SocketPublisher(threading.Thread):
    def __init__(self):
        """ Class which makes unicast to a list of sockets possible. To add a socket use registerListener. If you want to send a message to all the listeners
        """
        threading.Thread.__init__(self)
        self.listeners: List[Listener] = []
        self.message_queue = Queue()
        self.stop_event = threading.Event()

    def registerListener(self, host: str, port: int):
        """Register a new listener.

        :param host: IPv4 Adress
        :type host: str
        :param port: Port
        :type port: int
        :param message_type: Dataclass type with implemented fromDict method
        :type message_type: dataclass
        """
        listener = Listener(host, port)
        self.listeners.append(listener)

    def appendMessage(self, message: Type[T]):
        """Append a message to the queue."""
        self.message_queue.put(message)

    def run(self):
        """Start listening to incoming connections and publishing messages to listeners."""
        while True:
            if self.stop_event.is_set():
                break
            if not self.message_queue.empty():
                message = self.message_queue.get()
                for listener in self.listeners:
                    unreachable = []
                    try:
                        message_json = json.dumps(message, cls=EnhancedJSONEncoder).encode()
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((listener.host, listener.port))
                            s.sendall(message_json)
                    except ConnectionRefusedError:
                        print("Failed to establish connection removing socket host (ConnectionRefusedError)")
                        unreachable.append(listener)
                        pass
                self.listeners = [listener for listener in self.listeners if listener not in unreachable]

    def shutdown(self):
        self.stop_event.set()


if __name__ == "__main__":
    pub = SocketPublisher()
    pub.start()
    pub.registerListener("localhost", 12003)
    i = 0
    while True:
        i += 1
        pub.appendMessage(Coordinate(i, 3))
        sleep(0.2)
        print(i)