from collections import defaultdict

from middleware.types.MessageTypes import AddEntriesRequest
from states.State import State


class Leader(State):

    def __init__(self):
        self.nextIndexes = defaultdict(int)
        self.matchIndex = defaultdict(int)

    def setNode(self, node):
        print("(Leader) setNode")
        super().setNode(node)
        self.sendHeartbeat()
        # more logic...

    def onResponseReceived(self, message):
        print("onResponseReceived")
        # logic... (e.g. update state based on follower's response)
        return self, None

    def sendHeartbeat(self):
        print("(Leader) sendHeartbeat")
        message = AddEntriesRequest(
            senderID=self.node.id,
            receiverID=None,
            term=self.node.currentTerm,
            commitIndex=self.node.commitIndex,
            prevLogIndex=len(self.node.log)-1,
            prevLogTerm=self.node.log[-1].term if self.node.log else 0,
            entries=[(5, "command_1"), (6, "command_2"), (7, "command_3")]
        )
        self.node.sendMessageBroadcast(message)
