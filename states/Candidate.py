

class Candidate(Voter):
    def setNode(self, server):
        super().setNode(self, server)
        self.votes = {}
        self.startElection()

    def onVoteRequestReceived(self, message):
        return self, None

    def onVoteResponseReceived(self, message):
        # logic ...
        return self, None

    def startElection(self):
        self.node.currentTerm += 1
        # logic ...