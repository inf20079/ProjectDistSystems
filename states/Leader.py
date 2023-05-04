import json
import threading
import time
from collections import defaultdict

from middleware.types.JsonCoding import EnhancedJSONEncoder
from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse, RequestVoteMessage, LogEntry, \
    NavigationRequest, NavigationResponse, Member
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
            action=message
        )
        self.newEntries.append(newEntry)
        self.node.appendEntryToLog(newEntry)

        return self.__class__, None

    def onAppendEntriesResponseReceived(self, message: AppendEntriesResponse):
        print(f"[{self.node.id}](Leader) onAppendEntriesResponseReceived: {message}")

        if message.senderID not in self.nextIndex.keys():
            self.nextIndex[message.senderID] = self.node.lastLogIndex() + 1
        if message.senderID not in self.matchIndex.keys():
            self.matchIndex[message.senderID] = 0

        if not message.success:  # AppendEntries did not succeed
            if self.node.lastLogIndex() > -1:  # We can actually send a past log (maybe we just shouldn't be the Leader)
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
        print(message.senderID)

        #if self.nextIndex[message.senderID] > self.prevLogIndex:
        #    self.nextIndex[message.senderID] = self.prevLogIndex

        # If there exists an N such that N > commitIndex, a majority of matchIndex[i] >= N,
        # and log[N].term == currentTerm: set commitIndex = N.
        canCommit = False
        for N in range(self.node.commitIndex + 1, self.node.lastLogIndex() + 1):
            matchIndexCount = 0
            for matchIndex in self.matchIndex.values():
                if matchIndex >= N:
                    matchIndexCount += 1
            majority = matchIndexCount >= len(self.node.peers) // 2

            # print(f"[{self.node.id}](Leader) onAppendEntriesResponseReceived: {majority=}")
            if majority and self.node.log[N].term == self.node.currentTerm:
                canCommit = True
                break

        print(f"[{self.node.id}](Leader) onAppendEntriesResponseReceived: {canCommit=}")

        if canCommit:  # AppendEntries-RPC, apply changes to state machine, send response and commit.
            for i in range(self.node.lastApplied + 1, self.node.lastLogIndex() + 1):
                navigationRequest, nextStep = self.applyLogAtIndexToStateMachine(i)
                # print(f"[{self.node.id}](Leader) onAppendEntriesResponseReceived: Applying index {i}")
                if navigationRequest is None or nextStep is None:
                    continue

                navigationResponse = NavigationResponse(
                    clientId=navigationRequest.clientId,
                    leader=Member(
                        host=self.node.ipAddress,
                        port=self.node.unicastPort,
                        id=None
                    ),
                    nextStep=nextStep
                )
                self.node.sendMessageUnicast(navigationResponse, host=navigationRequest.clientHost,
                                             port=navigationRequest.clientPort)
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
