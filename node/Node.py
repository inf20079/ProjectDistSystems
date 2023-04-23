

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