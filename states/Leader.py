import json
import threading
import time
from collections import defaultdict

from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse, RequestVoteMessage, LogEntry, \
    NavigationRequest, NavigationResponse
from node.RecurringProcedure import RecurringProcedure
from states.State import State


class Leader(State):

    def __init__(self, node):
        super().__init__(node)
        self.nextIndex = {}  # for each server, index of the next log entry to send to that server
        self.matchIndex = {}  # for each server, index of highest log entry known to be replicated on server

        self.resetNewEntries()

        heartbeatTimeout = 0.1
        self.recurringProcedure = RecurringProcedure(heartbeatTimeout, self.sendHeartbeat)

        # Upon election: send initial heartbeat
        self.sendHeartbeat()
        self.recurringProcedure.start()

    def onClientRequestReceived(self, message: NavigationRequest):
        print(f"[{self.node.id}](Leader) onClientRequestReceived: {message}")

        newEntry = LogEntry(
            term=self.node.currentTerm,
            action=json.dumps(message, cls=EnhancedJSONEncoder)
        )
        self.newEntries.append(newEntry)
        self.node.log.append(newEntry)

        return self.__class__, None

    def onAppendEntriesResponseReceived(self, message: AppendEntriesResponse):
        print(f"[{self.node.id}](Leader) onAppendEntriesResponseReceived: {message}")

        if message.senderID not in self.nextIndex.keys():
            self.nextIndex[message.senderID] = self.node.lastLogIndex() + 1
        if message.senderID not in self.matchIndex.keys():
            self.matchIndex[message.senderID] = 0

        if not message.success:  # AppendEntries did not succeed
            if self.node.prevLogIndex > -1:  # We can actually send a past log (maybe we just shouldn't be the Leader)
                self.nextIndex[message.senderID] = max(0, self.nextIndex[message.senderID] - 1)

                previousIndex = self.nextIndex[message.senderID]
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

        self.matchIndex[message.senderID] = self.prevLogIndex
        self.nextIndex[message.senderID] = self.node.lastLogIndex() + 1

        if self.nextIndex[message.senderID] > self.prevLogIndex:
            self.nextIndex[message.senderID] = self.prevLogIndex

        # If there exists an N such that N > commitIndex, a majority of matchIndex[i] >= N,
        # and log[N].term == currentTerm: set commitIndex = N.
        canCommit = False
        for N in range(self.node.commitIndex + 1, self.node.lastLogIndex() + 1):
            matchIndexCount = 0
            for matchIndex in self.matchIndex:
                if matchIndex >= N:
                    matchIndexCount += 1
            majority = matchIndexCount >= len(self.node.peers) // 2
            if majority and self.node.log[N].term == self.node.currentTerm:
                canCommit = True
                break

        if canCommit:  # If the majority of nodes consented the
            # AppendEntries-RPC, apply changes to state machine, send response and commit.
            print(f"[{self.node.id}](Leader) onAppendEntriesResponseReceived: Can commit")
            for i in range(self.prevLogIndex, self.node.lastLogIndex() + 1):
                self.applyLogAtIndexToStateMachine(i)
            self.node.commitIndex = self.node.lastLogIndex()  # Commit
            self.node.lastApplied = self.node.commitIndex  # All that Leader commits is also applied

        return self.__class__, None

    def sendHeartbeat(self):
        print(f"[{self.node.id}](Leader) sendHeartbeat")
        message = AppendEntriesRequest(
            senderID=self.node.id,
            receiverID=-1,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=self.prevLogIndex,
            prevLogTerm=self.prevLogTerm,
            entries=self.newEntries
        )
        self.resetNewEntries()
        self.node.sendMessageBroadcast(message)
        self.recurringProcedure.resetTimeout()

    def resetNewEntries(self):
        self.newEntries = []
        self.prevLogIndex = self.node.lastLogIndex()
        self.prevLogTerm = self.node.lastLogTerm()

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        return self.__class__, self.generateVoteResponseMessage(message, False)

    def shutdown(self):
        # print(f"[{self.node.id}](Leader) shutdown")
        self.recurringProcedure.shutdown()
