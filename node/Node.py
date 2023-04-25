import threading
import time
from socket import gethostname, gethostbyname
from typing import Any

from middleware.BroadcastInterface import BroadcastInterface
from middleware.MulticastPublisher import MulticastPublisher
from middleware.UnicastListener import UnicastListener
from middleware.UnicastPublisher import UnicastPublisher, Unicast
from middleware.types.MessageTypes import RequestDiscover, ResponseDiscover, Member, LogEntry, Message


class Node:

    def __init__(self, id, state, ipAddress=None, broadcastPort=None, unicastPort=None, peers=None, log=None):
        # middleware
        self.ipAddress = ipAddress or gethostbyname(gethostname())
        self.broadcastPort = broadcastPort or 12004
        self.unicastPort = unicastPort or 12005
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

        self.peers = peers if peers is not None else {}

        self.isPeriodicDiscoveryActive = True
        self.discoveryInterval = 5
        threading.Thread(
            target=self.periodicDiscovery
        )

        self.state.setNode(self)

    def pollMessages(self):
        def handleQueue(interface):
            message = interface.popMessage()
            while message is not None:
                if message.senderID is not self.id:
                    if isinstance(message, RequestDiscover):
                        self.onDiscoveryRequest(message)
                    elif isinstance(message, ResponseDiscover):
                        self.onDiscoveryResponseReceived(message)
                    else:
                        self.onRaftMessage(message)
                message = interface.popMessage()

        handleQueue(self.unicastList)
        handleQueue(self.broadcastInterface)


    def periodicDiscovery(self):
        while self.isPeriodicDiscoveryActive:
            self.sendDiscovery()
            time.sleep(self.discoveryInterval)


    def lastLogIndex(self):
        return len(self.log) - 1 if len(self.log) > 0 else -1

    def lastLogTerm(self):
        return self.log[-1].term if len(self.log) > 0 else 0

    def sendMessageBroadcast(self, message: Any):
        print(f"[{self.id}](Node) sendMessageBroadcast")
        self.broadcastInterface.appendMessage(message)

    def sendMessageMulticast(self, message: Any):
        self.multicastPub.appendMessage(message)

    def sendMessageUnicast(self, message: Message):
        print(f"[{self.id}](Node) sendMessageUnicast")
        receiver = self.getIpByID(message.receiverID)
        unicast = Unicast(receiver.host, receiver.port, message)
        self.unicastPub.appendMessage(unicast)

    def manuallySwitchState(self, state):
        if self.state is not state:
            # print("manuallySwitchState")
            self.state.shutdown()
            state.setNode(self)
            self.state = state

    def onRaftMessage(self, message):
        print(f"[{self.id}](Node) onRaftMessage from {message.senderID} to {message.receiverID}")
        state, response = self.state.onMessage(message)

        if response is not None:
            self.sendMessageUnicast(response)

        self.manuallySwitchState(state)

        return state, response

    def getIpByID(self, id: int) -> Member:
        return [member for member in self.peers if member.id == id][0]

    def sendDiscovery(self):
        message = RequestDiscover(Member(id=self.id, host=self.ipAddress, port=self.unicastPort))
        self.broadcastInterface.appendMessage(message)

    def onDiscoveryResponseReceived(self, message: ResponseDiscover):
        self.peers = self.peers | {message.member}
        self.peers = self.peers | message.memberList

    def onDiscoveryRequest(self, message: RequestDiscover):
        message = ResponseDiscover(member=Member(self.ipAddress, self.unicastPort),
                                   memberList=self.peers)
        unicast = Unicast(message.member.host, message.member.port)
        self.sendMessageUnicast(unicast)

    def shutdown(self):
        self.state.shutdown()

        self.multicastPub.shutdown()
        self.multicastPub.join()
        self.unicastPub.shutdown()
        self.unicastPub.join()
        self.broadcastInterface.shutdown()
        self.broadcastInterface.join()
        self.unicastList.shutdown()
        self.unicastList.join()

        self.isPeriodicDiscoveryActive = False
