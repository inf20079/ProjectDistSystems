import abc
import socket
from typing import Any

from middleware.types.MessageTypes import *


class AbstractSocketInterface(abc.ABC):
    def __init__(self, serverIp: str, serverPort: int):
        """ Instantiates AbstractSocketListener: listens on port for incoming messages.

        :param host: IPv4 Adress
        :type host: str
        :param port: Port
        :type port: int
        """
        self.ip = "127.0.0.1" if serverPort == "localhost" else serverIp
        self.port = serverPort
        self.socket = self.configureSocket()
        self.receiveQueue = []
        self.sendQueue = []

    @abc.abstractmethod
    def configureSocket(self) -> socket.socket:
        pass

    def popMessage(self):
        """ Pops message element from queue

        :return: Dataclass element
        :rtype: dataclass
        """
        try:
            return self.receiveQueue.pop(0)
        except IndexError:
            return None

    def appendMessage(self, message: Any):
        self.sendQueue.append(message)

    @abc.abstractmethod
    def onReadable(self):
        pass

    @abc.abstractmethod
    def onWritable(self):
        pass

    @abc.abstractmethod
    def refresh(self):
        pass

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
        try:
            return NavigationRequest.fromDict(message)
        except TypeError:
            pass
        try:
            return NavigationResponse.fromDict(message)
        except TypeError:
            pass
