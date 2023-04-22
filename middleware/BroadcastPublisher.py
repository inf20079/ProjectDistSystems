import socket
import json
from time import sleep

from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate


class BroadcastPublisher:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", port))

    def broadcast(self, data):
        message = json.dumps(data, cls=EnhancedJSONEncoder)
        self.sock.sendto(message.encode(), ("<broadcast>", self.port))


if __name__ == "__main__":
    broadcaster = BroadcastPublisher(12003)
    i = 0
    while True:
        i += 1
        broadcaster.broadcast(Coordinate(i, 2))
        print(i)
        sleep(0.2)
