import socket
import json
import threading
from dataclasses import dataclass
from time import sleep
from typing import Any

import select

from middleware.AbstractSocketInterface import AbstractSocketInterface
from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import Coordinate


@dataclass
class Unicast:
    host: str
    port: int
    message: Any


class UnicastInterface(AbstractSocketInterface):

    def __init__(self, serverIp: str, serverPort: int):
        super().__init__(serverPort=serverPort, serverIp=serverIp)
        self.sendQueue = {}
        self.clientSockets = []
        self.clientThreads = []

    def configureSocket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(5)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def appendMessage(self, message: Unicast):
        if message.host == "localhost":
            message.host = "127.0.0.1"
        if message.host+str(message.port) in self.sendQueue:
            self.sendQueue[message.host + str(message.port)].append(message.message)
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((message.host, message.port))
        except ConnectionRefusedError as e:
            print(f"Failed to establish connection to message will not be sent: {str(e)}")
        sock.setblocking(False)
        self.clientSockets.append(sock)
        self.sendQueue[message.host + str(message.port)] = [message.message]

    def onWritable(self, sock):
        remoteAddress, remotePort = sock.getpeername()
        try:
            sendQueue = self.sendQueue[remoteAddress+str(remotePort)]
        except KeyError:
            self.clientSockets.remove(sock)
            print(f"KeyError: For Socket({remoteAddress}, {remotePort}) are no messages to send.")
            return
        if not sendQueue:
            self.clientSockets.remove(sock)
            del self.sendQueue[remoteAddress+str(remotePort)]
            print(f"List Empty: For Socket({remoteAddress}, {remotePort}) are no messages to send.")
            return
        for message in sendQueue:
            message_json = json.dumps(message, cls=EnhancedJSONEncoder).encode()
            try:
                sock.sendall(message_json)
            except ConnectionResetError as e:
                print(f"{e}")
                break
        del self.sendQueue[remoteAddress+str(remotePort)]
        self.clientSockets.remove(sock)

    def onReadable(self):
        client_socket, addr = self.socket.accept()
        client_thread = threading.Thread(target=self.listenToClient, args=(client_socket,))
        client_thread.start()
        self.clientThreads.append(client_thread)

    def listenToClient(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            message_parsed = self.parseMessage(message)
            self.receiveQueue.append(message_parsed)
        client_socket.close()

    def refresh(self):
        readable, writable, _ = select.select([self.socket], self.clientSockets, [], 0.0001)
        # send messages
        for sock in writable:
            self.onWritable(sock)
        # receive messages
        if readable:
            self.onReadable()

    def __del__(self):

        # close socket
        self.socket.close()
        # Clean up client threads
        if not self.clientThreads:
            return
        for thread in self.clientThreads:
            thread.join()


if __name__ == "__main__":
    interface = UnicastInterface("localhost", 14008)
    i = 0
    while i <= 5:
        i += 1
        interface.appendMessage(Unicast("localhost", 14008, Coordinate(i, 2)))
        print("Send", interface.sendQueue)
        interface.refresh()
        print("Receive", interface.receiveQueue)
