from collections import defaultdict

from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse
from states.State import State


class Leader(State):

    def __init__(self):
        self.nextIndexes = {}
        self.matchIndexes = {}

    def setNode(self, node):
        print("(Leader) setNode")
        super().setNode(node)

        self.nextIndexes = {peer: len(node.log) for peer in node.peers}
        self.matchIndexes = {peer: 0 for peer in node.peers}

        self.sendHeartbeat()

    def onResponseReceived(self, message: AppendEntriesResponse):
        print("onResponseReceived")

        if (message.success):
            self.matchIndexes[message.senderID]

        return self, None

    def sendHeartbeat(self):
        print("(Leader) sendHeartbeat")
        message = AppendEntriesRequest(
            senderID=self.node.id,
            receiverID=None,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=len(self.node.log)-1,
            prevLogTerm=self.node.log[-1].term if self.node.log else 0,
            entries=[(5, "command_1"), (6, "command_2"), (7, "command_3")]
        )
        self.node.sendMessageBroadcast(message)

