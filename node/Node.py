

class Node:

    def __init__(self, id, state):
        self.id = id
        self.state = state
        self.log = []  # logEntry = [( 2: 'do something'), ...]

        self.commitIndex = 0
        self.currentTerm = 0

        self.state.setNode(self)

        self.peers = {}
        # ToDo: Discover peers.

    def lastLogIndex(self):
        return len(self.log)-1 if len(self.log) > 0 else -1

    def lastLogTerm(self):
        return self.log[-1].term if len(self.log) > 0 else 0

    def sendMessageBroadcast(self, message):
        print("(Node) sendMessageBroadcast")
        # ToDo: Broadcast
        pass

    def sendMessageMulticast(self, message):
        # ToDo: Multicast
        pass

    def sendMessageUnicast(self, message):
        # ToDo: Unicast
        pass

    def onMessage(self, message):
        state, response = self.state.onMessage(message)
        self.state = state

        return state, response