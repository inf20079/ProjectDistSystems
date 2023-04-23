from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse
from states.Voter import Voter


class Follower(Voter):

    def __init__(self):
        Voter.__init__(self)
        self.leaderID = None

    def onAppendEntries(self, message: AppendEntriesRequest):
        self.resetElectionTimeout()
        return super().onAppendEntries(message)
