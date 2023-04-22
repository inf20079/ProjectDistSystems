from dataclasses import dataclass


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
    term: int

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
class AddEntryMessage(Message):
    commit: bool
    success: bool  # false rejects, true if logs match
    newLogEntry: str
    lastLogIndex: int

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.commit=}, {self.success=}, {self.lastLogIndex=}, {self.newLogEntry=})"

@dataclass(frozen=True)
class LeaderResponseMessage(Message):

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=})"


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
