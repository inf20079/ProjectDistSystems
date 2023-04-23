from socket import gethostname, gethostbyname
from typing import Any

from middleware.BroadcastInterface import BroadcastInterface
from middleware.MulticastPublisher import MulticastPublisher
from middleware.UnicastListener import UnicastListener
from middleware.UnicastPublisher import UnicastPublisher
from middleware.types.MessageTypes import RequestDiscover, ResponseDiscover, Member
from dataclasses import dataclass
import socket


@dataclass(frozen=True)
class LogEntry:
    term: int
    action: str

    
class Node:

    def __init__(self, id, state, startPort=None, peers=None, log=None):
        # middleware
        hostname = gethostname()
        self.ipAddress = gethostbyname(hostname)
        self.broadcastPort = 12004
        self.unicastPort = 12005
        ## Interface
        self.broadcastInterface = BroadcastInterface(self.broadcastPort)
        self.broadcastInterface.start()
        ## publisher
        self.multicastPub = MulticastPublisher()
        self.multicastPub.start()
        self.unicastPub = UnicastPublisher()
        self.unicastPub.start()
        ## listener
        self.unicastList = UnicastListener(host=self.ipAddress, port=self.unicastPort)
        self.unicastList.start()

        # raft
        self.id = id
        self.state = state
        self.log: [LogEntry] = [] if log is None else log

        self.commitIndex = 0
        self.currentTerm = 0

        self.peers = {} if peers is None else peers

        self.state.setNode(self)

        self.peers = {}

    def lastLogIndex(self):
        return len(self.log) - 1 if len(self.log) > 0 else -1

    def lastLogTerm(self):
        return self.log[-1].term if len(self.log) > 0 else 0

    def sendMessageBroadcast(self, message: Any):
        self.broadcastInterface.appendMessage(message)

    def sendMessageMulticast(self, message: Any):
        self.multicastPub.appendMessage(message)

    def sendMessageUnicast(self, message: Any):
        self.unicastPub.appendMessage(message)

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

    def getIpByID(self, id: int):
        return [member for member in self.peers if member.id == id]

    def sendDiscovery(self):
        message = RequestDiscover(Member(senderID=self.id, host=self.ipAddress, port=self.unicastPort))
        self.broadcastInterface.appendMessage(message)

    def onDiscoveryResponseReceived(self, message: ResponseDiscover):
        self.peers = self.peers | {message.member}
        self.peers = self.peers | message.memberList

    def shutdown(self):
        self.multicastPub.shutdown()
        self.multicastPub.join()
        self.unicastPub.shutdown()
        self.unicastPub.join()
        self.broadcastInterface.shutdown()
        self.broadcastInterface.join()
        self.unicastList.shutdown()
        self.unicastList.join()

