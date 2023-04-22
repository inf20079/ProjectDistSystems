from dataclasses import dataclass
from typing import List, Tuple


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
class AddEntriesRequest(Message):
    commitIndex: int  # The index of the highest log entry that the leader knows to be committed
    prevLogIndex: int  # The index of the log entry immediately preceding the new entries being appended
    prevLogTerm: int  # The term of the prevLogIndex
    entries: List[Tuple[int, str]]  # A list of new log entries to be appended to the log

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.commitIndex=}, {self.prevLogIndex=}, {self.prevLogTerm=}, {self.entries=})"


@dataclass(frozen=True)
class AddEntriesResponse(Message):
    success: bool
    conflictIndex: int
    conflictTerm: int

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.success=}, {self.conflictIndex=}, {self.conflictTerm=})"


@dataclass(frozen=True)
class VoteMessage(Message):
    vote = None  # None to request, 1 vote yes, 0 vote no

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.vote=})"


@dataclass(frozen=True)
class RequestVoteMessage(VoteMessage):
    vote = None


@dataclass(frozen=True)
class ResponseVoteMessage(VoteMessage):
    vote: int  # 1 vote yes, 0 vote no
