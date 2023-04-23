import abc
from queue import Queue
import threading
import socket

from middleware.types.MessageTypes import *


class AbstractSocketListener(abc.ABC, threading.Thread):
    def __init__(self, host: str, port: int):
        """ Instantiates AbstractSocketListener: listens on port for incoming messages.

        :param host: IPv4 Adress
        :type host: str
        :param port: Port
        :type port: int
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = self.configureSocket()
        self.client_threads = []
        self.message_queue = Queue()
        self.stop_event = threading.Event()

    @abc.abstractmethod
    def configureSocket(self) -> socket.socket:
        pass

    def popMessage(self):
        """ Pops message element from queue

        :return: Dataclass element
        :rtype: dataclass
        """
        if self.message_queue.empty():
            return None
        else:
            return self.message_queue.get()

    @staticmethod
    def parseMessage(message):
        """ Parses JSON dict into dataclasses defined in MessageTypes

        :param message: JSON dict
        :type message: dict
        :return: MessageType type
        :rtype: dataclass
        """
        try:
            return Coordinate.fromDict(message)
        except TypeError:
            pass
        try:
            return Message.fromDict(message)
        except TypeError:
            pass
        try:
            return AppendEntriesRequest.fromDict(message)
        except TypeError:
            pass
        try:
            return AppendEntriesResponse.fromDict(message)
        except TypeError:
            pass
        try:
            return RequestVoteMessage.fromDict(message)
        except TypeError:
            pass
        try:
            return ResponseVoteMessage.fromDict(message)
        except TypeError:
            pass
        try:
            return Member.fromDict(message)
        except TypeError:
            pass
        try:
            return RequestDiscover.fromDict(message)
        except TypeError:
            pass
        try:
            return ResponseDiscover.fromDict(message)
        except TypeError:
            pass

    @abc.abstractmethod
    def run(self):
        pass

    def shutdown(self):
        self.socket.close()
        self.stop_event.set()
