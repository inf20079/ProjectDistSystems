from collections import defaultdict

from states.State import State


class Leader(State):

    def __init__(self):
        self.nextIndexes = defaultdict(int)
        self.matchIndex = defaultdict(int)

    def setNode(self, node):
        super().setNode(node)
        # more logic...

    def onResponseReceived(self, message):
        print("onResponseReceived")
        # logic...
        return self, None

    def sendHeartBeat(self):
        pass