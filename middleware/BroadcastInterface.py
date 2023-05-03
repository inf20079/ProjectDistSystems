import json
import socket
from time import sleep

import select

from middleware.AbstractSocketInterface import AbstractSocketInterface
from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate


class BroadcastInterface(AbstractSocketInterface):

    def __init__(self, port: int):
        super().__init__(serverPort=port, serverIp="")

    def configureSocket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((self.ip, self.port))
        return sock

    def onReadable(self):
        data, address = self.socket.recvfrom(1024)
        print(data)
        if not data:
            return
        message = json.loads(data.decode())
        message_parsed = self.parseMessage(message)
        self.receiveQueue.append(message_parsed)

    def onWritable(self):
        while self.sendQueue:
            message = self.sendQueue.pop(0)
            message_json_string = json.dumps(message, cls=EnhancedJSONEncoder)
            self.socket.sendto(message_json_string.encode(), ("<broadcast>", self.port))

    def refresh(self):
        readable, writable, _ = select.select([self.socket], [self.socket], [], 0.1)
        # send messages
        if writable:
            self.onWritable()
        # receive messages
        if readable:
            self.onReadable()

    def __del__(self):
        self.socket.close()


if __name__ == "__main__":
    interface = BroadcastInterface(12003)
    i = 0
    while i <= 5:
        i += 1
        interface.appendMessage(Coordinate(i, 2))
        print(interface.sendQueue)
        interface.refresh()
        print(interface.receiveQueue)
        sleep(0.5)
