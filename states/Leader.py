import threading
import time
from collections import defaultdict

from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse, RequestVoteMessage, LogEntry, \
    ClientRequestMessage
from node.RecurringProcedure import RecurringProcedure
from states.State import State


class Leader(State):

    def __init__(self, node):
        super().__init__(node)
        self.nextIndex = {}  # for each server, index of the next log entry to send to that server
        self.matchIndex = {}  # for each server, index of highest log entry known to be replicated on server

        heartbeatTimeout = 0.1
        self.recurringProcedure = RecurringProcedure(heartbeatTimeout, self.sendHeartbeat)

        # Upon election: send initial heartbeat
        self.sendHeartbeat()
        self.recurringProcedure.start()

    def onClientRequestReceived(self, message: ClientRequestMessage):
        print(f"[{self.node.id}](Leader) onClientRequestReceived: {message}")

        # ToDo: Logic

        newEntries = [
            LogEntry(
                term=self.node.currentTerm,
                action="Give you up"
            ),
            LogEntry(
                term=self.node.currentTerm,
                action="Let you down"
            ),
            LogEntry(
                term=self.node.currentTerm,
                action="Run around"
            ),
            LogEntry(
                term=self.node.currentTerm,
                action="Desert you"
            )
        ]

        prevLogIndex = self.node.lastLogIndex()
        prevLogTerm = self.node.lastLogTerm()

        self.node.log += newEntries
        self.node.commitIndex = self.node.lastLogIndex()

        appendEntriesMessage = AppendEntriesRequest(
            senderID=self.node.id,
            receiverID=-1,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=prevLogIndex,
            prevLogTerm=prevLogTerm,
            entries=newEntries
        )
        self.node.sendMessageBroadcast(appendEntriesMessage)

        return self.__class__, None

    def onResponseReceived(self, message: AppendEntriesResponse):
        print(f"[{self.node.id}](Leader) onResponseReceived: {message}")

        if message.senderID not in self.nextIndex.keys():
            self.nextIndex[message.senderID] = self.node.lastLogIndex() + 1
        if message.senderID not in self.matchIndex.keys():
            self.matchIndex[message.senderID] = 0

        if not message.success:
            self.nextIndex[message.senderID] -= 1

            previousIndex = max(0, self.nextIndex[message.senderID] - 1)
            previous = self.node.log[previousIndex]
            current = self.node.log[self.nextIndex[message.senderID]]

            appendEntry = AppendEntriesRequest(
                senderID=self.node.id,
                receiverID=message.senderID,
                term=self.node.currentTerm,
                commitIndex=self.node.commitIndex,
                prevLogIndex=previousIndex,
                prevLogTerm=previous.term,
                entries=[current]
            )
            return self.__class__, appendEntry
        else:
            self.nextIndex[message.senderID] += 1

            if self.nextIndex[message.senderID] > self.node.lastLogIndex():
                self.nextIndex[message.senderID] = self.node.lastLogIndex()

            return self.__class__, None

    def sendHeartbeat(self):
        print(f"[{self.node.id}](Leader) sendHeartbeat")
        message = AppendEntriesRequest(
            senderID=self.node.id,
            receiverID=-1,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=len(self.node.log) - 1,
            prevLogTerm=self.node.lastLogTerm(),
            entries=[]
        )
        self.node.sendMessageBroadcast(message)
        self.recurringProcedure.resetTimeout()

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        return self.__class__, self.generateVoteResponseMessage(message, False)

    def shutdown(self):
        # print(f"[{self.node.id}](Leader) shutdown")
        self.recurringProcedure.shutdown()
