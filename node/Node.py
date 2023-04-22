

class Node:

    def __init__(self, id, state, log):
        self.id = id
        self.state = state
        self.log = log  # logEntry = { 'term': 2, 'command': 'do something }

        self.commitIndex = 0
        self.currentTerm = 0

        self.state.setNode(self)

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