from dataclasses import dataclass
from typing import List


class Node:

    def __init__(self, id, state, peers=None, log=None):
        self.id = id
        self.state = state
        self.log: [LogEntry] = [] if log is None else log

        self.commitIndex = 0
        self.currentTerm = 0

        self.peers = {} if peers is None else peers

        self.state.setNode(self)
        # ToDo: Discover peers.

    def lastLogIndex(self):
        return len(self.log) - 1 if len(self.log) > 0 else -1

    def lastLogTerm(self):
        return self.log[-1].term if len(self.log) > 0 else 0

    def sendMessageBroadcast(self, message):
        print("(Node) sendMessageBroadcast")
        # ToDo: Broadcast
        pass

    def sendMessageMulticast(self, message):
        # ToDo: Multicast
        pass

    def sendMessageUnicast(self, message):
        # ToDo: Unicast
        pass

    def onMessage(self, message):
        state, response = self.state.onMessage(message)
        self.state = state

        return state, response


@dataclass(frozen=True)
class LogEntry:
    term: int
    action: str
