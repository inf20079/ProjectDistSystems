from collections import defaultdict

from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse
from states.State import State


class Leader(State):

    def __init__(self):
        self.nextIndex = {}  # for each server, index of the next log entry to send to that server
        self.matchIndex = {}  # for each server, index of highest log entry known to be replicated on server

    def setNode(self, node):
        print("(Leader) setNode")
        super().setNode(node)

        self.nextIndex = {peer: (self.node.lastLogIndex() + 1) for peer in node.peers}
        self.matchIndex = {peer: 0 for peer in node.peers}

        # Upon election: send initial heartbeat
        self.sendHeartbeat()

    def onResponseReceived(self, message: AppendEntriesResponse):
        print("(Leader) onResponseReceived")

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
        print("(Leader) sendHeartbeat")
        message = AppendEntriesRequest(
            senderID=self.node.id,
            receiverID=None,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=len(self.node.log)-1,
            prevLogTerm=self.node.lastLogTerm(),
            entries=[(5, "command_1"), (6, "command_2"), (7, "command_3")]
        )
        self.node.sendMessageBroadcast(message)
