from dataclasses import dataclass
from typing import List, Set

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

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


@dataclass()
class NavigationRequest:
    clientId: int
    clientHost: str
    clientPort: int
    currentPosition: Coordinate
    destination: Coordinate

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        try:
            dict["currentPosition"] = Coordinate(**dict["currentPosition"])
            dict["destination"] = Coordinate(**dict["destination"])
            return cls(**dict)
        except KeyError as e:
            raise TypeError(str(e))

    def __repr__(self):
        return f"NavigationRequest({self.clientId=}, {self.clientHost=}, {self.clientPort=}, {self.currentPosition=}, {self.destination=})"


@dataclass(frozen=True)
class LogEntry:
    term: int
    action: NavigationRequest

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        dict["action"] = NavigationRequest.fromDict(dict["action"])
        return cls(**dict)

    def __repr__(self):
        return f"LogEntry({self.term=}, {self.action=})"


@dataclass(frozen=False)
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


@dataclass(frozen=False)
class AppendEntriesRequest(Message):
    commitIndex: int  # The index of the highest log entry that the leader knows to be committed
    prevLogIndex: int  # The index of the log entry immediately preceding the new entries being appended
    prevLogTerm: int  # The term of the prevLogIndex
    entries: List[LogEntry]  # A list of new log entries to be appended to the log

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        try:
            dict["entries"] = [LogEntry.fromDict(entry) for entry in dict["entries"]]
            return cls(**dict)
        except KeyError as e:
            raise TypeError(str(e))

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.commitIndex=}, {self.prevLogIndex=}, {self.prevLogTerm=}, {self.entries=})"


@dataclass(frozen=False)
class AppendEntriesResponse(Message):
    success: bool

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.success=})"


@dataclass(frozen=False)
class RequestVoteMessage(Message):
    lastLogIndex: int
    lastLogTerm: int

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.lastLogIndex=}, {self.lastLogTerm=})"


@dataclass(frozen=False)
class ResponseVoteMessage(Message):
    voteGranted: bool

    def __repr__(self):
        return f"Message({self.senderID=}, {self.receiverID=}, {self.term=}, {self.voteGranted=})"


@dataclass(frozen=True)
class Member:
    """ Member class used to initialize discover
    """
    id: int
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

    def __repr__(self):
        return f"Member({self.id=}, {self.host=}, {self.port=})"


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

    def __repr__(self):
        return f"RequestDiscover({self.member=})"


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
        try:
            dict["memberList"] = [Member(**entry) for entry in dict["memberList"]]
            return cls(**dict)
        except KeyError as e:
            raise TypeError(str(e))

@dataclass()
class NavigationResponse:
    clientId: int
    nextStep: Coordinate = None
    leader: Member = None

    @classmethod
    def fromDict(cls, dict):
        """ object creation from dict

        :param dict: coordinate dataclass as dict
        :type dict:
        :return:
        :rtype: coordinate dataclass
        """
        try:
            dict["nextStep"] = Coordinate(**dict["nextStep"])
            dict["leader"] = Member(**dict["leader"])
            return cls(**dict)
        except KeyError as e:
            raise TypeError(str(e))

    def __repr__(self):
        return f"NavigationResponse({self.clientId=}, {self.nextStep=})"
