from dataclasses import dataclass
from typing import List, Tuple, Set

from node.Node import LogEntry


@dataclass(frozen=True)
class Coordinate:
    """ Coordinate Dataclass
    """
    x: int = None
    y: int = None

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        return cls(**dict)

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"


@dataclass(frozen=True)
class Message:
    senderID: int
    receiverID: int
    term: int  # the term of the current leader

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        return cls(**dict)

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=})"


@dataclass(frozen=True)
class AppendEntriesRequest(Message):
    commitIndex: int  # The index of the highest log entry that the leader knows to be committed
    prevLogIndex: int  # The index of the log entry immediately preceding the new entries being appended
    prevLogTerm: int  # The term of the prevLogIndex
    entries: [LogEntry]  # A list of new log entries to be appended to the log

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.commitIndex=}, {self.prevLogIndex=}, {self.prevLogTerm=}, {self.entries=})"


@dataclass(frozen=True)
class AppendEntriesResponse(Message):
    success: bool

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.success=})"


@dataclass(frozen=True)
class RequestVoteMessage(Message):
    lastLogIndex: int
    lastLogTerm: int

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.lastLogIndex=}, {self.lastLogTerm=})"


@dataclass(frozen=True)
class ResponseVoteMessage(Message):
    voteGranted: bool

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.voteGranted=})"

@dataclass(frozen=True)
class Member:
    """ Member class used to initialize discover
    """
    senderID: int
    host: str
    port: int

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        return cls(**dict)

@dataclass(frozen=True)
class RequestDiscover:
    member: Member  # origin of the request

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        return cls(**dict)

@dataclass(frozen=True)
class ResponseDiscover:
    member: Member  # origin of the response
    memberList: Set[Member]  # List of known members

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        return cls(**dict)