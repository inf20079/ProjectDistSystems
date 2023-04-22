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
    status: str
    sender_id: int
    receiver_id: int
    data = None
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
        return f"Message({self.status=}, {self.sender_id=}, {self.receiver_id=}, {self.data=}, {self.term=})"


@dataclass(frozen=True)
class AddEntryMessage(Message):
    commit: bool
    success: bool  # false rejects, true if logs match
    last_log_index: int
    new_log_entry = None

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
        return f"Message({self.status=}, {self.sender_id=}, {self.receiver_id=}, {self.data=}, {self.term=}, {self.commit=}, {self.success=}, {self.last_log_index=}, {self.new_log_entry=})"


@dataclass(frozen=True)
class VoteMessage(Message):
    vote = None  # None to request, 1 vote yes, 0 vote no

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
        return f"Message({self.status=}, {self.sender_id=}, {self.receiver_id=}, {self.data=}, {self.term=}, {self.vote=})"


@dataclass(frozen=True)
class RequestVoteMessage(VoteMessage):
    vote = None

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
        return f"Message({self.status=}, {self.sender_id=}, {self.receiver_id=}, {self.data=}, {self.term=}, {self.vote=})"


@dataclass(frozen=True)
class ResponseVoteMessage(VoteMessage):
    vote: int  # 1 vote yes, 0 vote no

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
        return f"Message({self.status=}, {self.sender_id=}, {self.receiver_id=}, {self.data=}, {self.term=}, {self.vote=})"
