import socket
import json
import threading
from queue import Queue
from time import sleep
from dataclasses import dataclass
from typing import Type, TypeVar

from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate

T = TypeVar("T")


@dataclass
class Unicast:
    host: str
    port: int
    message: Type[T]



class UnicastPublisher(threading.Thread):
    def __init__(self):
        """ Class which makes unicast to a list of sockets possible. To add a socket use registerListener. If you want to send a message to all the listeners
        """
        threading.Thread.__init__(self)
        self.message_queue: Queue[Unicast] = Queue()
        self.stop_event = threading.Event()
        self.send_threads = []

    def appendMessage(self, message: Unicast):
        """Append a message to the queue."""
        self.message_queue.put(message)

    def run(self):
        """Start listening to incoming connections and publishing messages to listeners."""
        while True:
            if self.stop_event.is_set():
                break
            if not self.message_queue.empty():
                unicast = self.message_queue.get()
                send_thread = threading.Thread(target=self.sendUnicast, args=(unicast,))
                send_thread.start()
                self.send_threads.append(send_thread)

            # Clean up client threads
            for thread in self.send_threads:
                thread.join()


    def sendUnicast(self, message: Unicast):
        try:
            message_json = json.dumps(message.message, cls=EnhancedJSONEncoder).encode()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((message.host, message.port))
                s.sendall(message_json)
        except ConnectionRefusedError as e:
            print(f"Failed to establish connection to message will not be sent: {str(e)}")


    def shutdown(self):
        self.stop_event.set()

    def __del__(self):
        # Clean up client threads
        for thread in self.send_threads:
            thread.join()

if __name__ == "__main__":
    pub = UnicastPublisher()
    pub.start()

    i = 0
    while True:
        i += 1
        pub.appendMessage(Unicast("localhost", 12005, Coordinate(i, 3)))
        sleep(0.2)
        print(i)