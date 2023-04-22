from states.Voter import Voter


class Candidate(Voter):
    def setNode(self, node):
        super().setNode(self, node)
        self.votes = {}
        self.startElection()

    def onVoteRequestReceived(self, message):
        return self, None

    def onVoteResponseReceived(self, message):
        print("onVoteResponseReceived")

        # logic ...
        return self, None

    def startElection(self):
        self.node.currentTerm += 1
        # logic ...