import inspect
import threading
import time
from socket import gethostname, gethostbyname
from typing import Any

from control.TrafficArea import TrafficArea
from control.TrafficControlLogic import TrafficControlLogic
from middleware.BroadcastInterface import BroadcastInterface
from middleware.UnicastInterface import UnicastInterface, Unicast
from middleware.types.MessageTypes import RequestDiscover, ResponseDiscover, Member, LogEntry, Message, \
    NavigationRequest, Coordinate


class Node:

    def __init__(self, id, stateClass, ipAddress=None, broadcastPort=None, unicastPort=None, peers=None, log=None):
        # middleware
        self.ipAddress = ipAddress or gethostbyname(gethostname())
        self.broadcastPort = broadcastPort or 12004
        self.unicastPort = unicastPort or 12005
        ## Interface
        self.broadcastInterface = BroadcastInterface(self.broadcastPort)
        self.unicastInterface = UnicastInterface(serverIp=self.ipAddress, serverPort=self.unicastPort)

        # raft
        self.id = id
        self.log: [LogEntry] = [] if log is None else log

        self.commitIndex = -1  # Nothing committed so far
        self.lastApplied = -1
        self.currentTerm = 0

        self.peers = peers if peers is not None else {}

        self.isPeriodicDiscoveryActive = True
        self.discoveryInterval = 5
        threading.Thread(
            target=self.periodicDiscovery
        )

        self.state = stateClass(self)
        print(self.state)

        # logic
        self.trafficControlLogic = TrafficControlLogic(TrafficArea(2, 1000, 1000))

    def pollMessages(self):
        self.unicastInterface.refresh()
        self.broadcastInterface.refresh()

        def handleQueue(interface):
            message = interface.popMessage()
            while message is not None:
                if isinstance(message, NavigationRequest):
                    self.state.onClientRequestReceived(message)
                elif message.senderID is not self.id:
                    if isinstance(message, RequestDiscover):
                        self.onDiscoveryRequest(message)
                    elif isinstance(message, ResponseDiscover):
                        self.onDiscoveryResponseReceived(message)
                    else:
                        self.onRaftMessage(message)
                message = interface.popMessage()

        handleQueue(self.unicastInterface)
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

    def sendMessageUnicast(self, message: Any, host: str = None, port: int = None):
        print(f"[{self.id}](Node) sendMessageUnicast: {message.receiverID=}")
        if host is None or port is None:
            receiver = self.getIpByID(message.receiverID)
            host = receiver.host
            port = receiver.port
        unicast = Unicast(host, port, message)
        self.unicastInterface.appendMessage(unicast)

    def manuallySwitchState(self, stateClass):
        if not inspect.isclass(stateClass):
            raise TypeError("ERROR: STATECLASS IS INSTANCE AND NOT CLASS")
        if not isinstance(self.state, stateClass):
            print(f"[{self.id}](Node) manuallySwitchState: from {self.state.__class__} to {stateClass}")
            self.state.shutdown()
            self.state = stateClass(self)

    def onRaftMessage(self, message):
        print(f"[{self.id}](Node) onRaftMessage from {message.senderID} to {message.receiverID}")
        stateClass, response = self.state.onRaftMessage(message=message)

        if response is not None:
            self.sendMessageUnicast(response)

        self.manuallySwitchState(stateClass)

        return stateClass, response

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

    def applyToStateMachine(self, message: NavigationRequest):
        print(f"[{self.id}](Node) applyToStateMachine")
        if message.currentPosition.x is None or message.currentPosition.y is None:
            self.trafficControlLogic.start(message.clientId)
        return self.trafficControlLogic.move(message.clientId, message.destination)


    def shutdown(self):
        self.state.shutdown()
        self.isPeriodicDiscoveryActive = False
