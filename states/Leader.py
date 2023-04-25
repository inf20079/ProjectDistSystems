import threading
import time
from collections import defaultdict

from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse, RequestVoteMessage, LogEntry
from node.RecurringProcedure import RecurringProcedure
from states.State import State


class Leader(State):

    def __init__(self):
        self.nextIndex = {}  # for each server, index of the next log entry to send to that server
        self.matchIndex = {}  # for each server, index of highest log entry known to be replicated on server
        self.heartbeatTimeout = 2  # 0.1
        self.heartbeatActive = True
        self.recurringProcedure = RecurringProcedure(self.heartbeatTimeout, self.sendHeartbeat)

    def setNode(self, node):
        print(f"[{node.id}](Leader) setNode")
        super().setNode(node)

        # Upon election: send initial heartbeat
        self.sendHeartbeat()
        self.recurringProcedure.start()


    def onResponseReceived(self, message: AppendEntriesResponse):
        print(f"[{self.node.id}](Leader) onResponseReceived")

        if message.senderID not in self.nextIndex:
            self.nextIndex[message.senderID] = self.node.lastLogIndex() + 1
        if message.senderID not in self.matchIndex:
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
            return self, appendEntry
        else:
            self.nextIndex[message.senderID] += 1
            print(self.nextIndex[message.senderID])

            if self.nextIndex[message.senderID] > self.node.lastLogIndex():
                self.nextIndex[message.senderID] = self.node.lastLogIndex()

            return self, None

    def sendHeartbeat(self):
        print(f"[{self.node.id}](Leader) sendHeartbeat")
        message = AppendEntriesRequest(
            senderID=self.node.id,
            receiverID=-1,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=len(self.node.log) - 1,
            prevLogTerm=self.node.lastLogTerm(),
            entries=[LogEntry(5, "command_1"), LogEntry(6, "command_2"), LogEntry(7, "command_3")]
        )
        self.node.sendMessageBroadcast(message)
        self.recurringProcedure.resetTimeout()


    def onVoteRequestReceived(self, message: RequestVoteMessage):
        return self, self.generateVoteResponseMessage(message, False)

    def shutdown(self):
        print(f"[{self.node.id}](Leader) shutdown")
        self.recurringProcedure.shutdown()
