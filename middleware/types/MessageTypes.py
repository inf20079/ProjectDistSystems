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


@dataclass(frozen=True)
class AddEntryMessage(Message):
    commit: bool
    success: bool  # false rejects, true if logs match
    newLogEntry = None
    lastLogIndex: int


@dataclass(frozen=True)
class VoteMessage(Message):
    vote = None  # None to request, 1 vote yes, 0 vote no


@dataclass(frozen=True)
class RequestVoteMessage(VoteMessage):
    vote = None


@dataclass(frozen=True)
class ResponseVoteMessage(VoteMessage):
    vote: int  # 1 vote yes, 0 vote no
