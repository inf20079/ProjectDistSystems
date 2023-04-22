from states.Voter import Voter


class Follower(Voter):

    def __init__(self, timeout=500):
        Voter.__init__(self)
        self.timeout = timeout
        self.timeoutTime = self.nextTimeout()

    def onAddEntries(self, message):
        print("onAddEntries")

        self.timeoutTime = self.nextTimeout()
        # logic...
        return self, None
