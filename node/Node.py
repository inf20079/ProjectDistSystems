from dataclasses import dataclass
import socket


class Node:

    def __init__(self, id, state, startPort=None, peers=None, log=None):
        self.id = id
        self.state = state
        self.log: [LogEntry] = [] if log is None else log

        self.commitIndex = 0
        self.currentTerm = 0

        self.peers = {} if peers is None else peers

        self.state.setNode(self)

        from middleware.BroadcastListener import BroadcastListener
        from middleware.BroadcastPublisher import BroadcastPublisher
        from middleware.UnicastListener import UnicastListener
        from middleware.UnicastPublisher import UnicastPublisher

        if startPort is not None:
            localAddress = socket.gethostbyname(socket.gethostname())
            self.broadcastListener = BroadcastListener(startPort + id * 4 + 0)
            self.broadcastPublisher = BroadcastPublisher(startPort + id * 4 + 1)
            self.unicastListener = UnicastListener(localAddress, startPort + id * 4 + 2)
            self.unicastPublisher = UnicastPublisher(localAddress, startPort + id * 4 + 3)
        # ToDo: Discover peers.

    def lastLogIndex(self):
        return len(self.log) - 1 if len(self.log) > 0 else -1

    def lastLogTerm(self):
        return self.log[-1].term if len(self.log) > 0 else 0

    def sendMessageBroadcast(self, message):
        # print("(Node) sendMessageBroadcast")
        # ToDo: Broadcast
        pass

    def sendMessageMulticast(self, message):
        # ToDo: Multicast
        pass

    def sendMessageUnicast(self, message):
        # ToDo: Unicast
        pass

    def manuallySwitchState(self, state):
        if self.state is not state:
            print("manuallySwitchState")
            self.state.shutdown()
            self.state = state
            state.setNode(self)

    def onMessage(self, message):
        state, response = self.state.onMessage(message)
        self.manuallySwitchState(state)

        return state, response


@dataclass(frozen=True)
class LogEntry:
    term: int
    action: str
