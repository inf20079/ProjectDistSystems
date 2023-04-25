from middleware.types.MessageTypes import AppendEntriesRequest
from states.Voter import Voter


class Follower(Voter):

    def __init__(self):
        Voter.__init__(self)
        self.leaderID = None

    def onAppendEntries(self, message: AppendEntriesRequest):
        self.recurringProcedure.resetTimeout()
        return super().onAppendEntries(message)

    def onElectionTimeouted(self):
        print(f"[{self.node.id}](Follower) onElectionTimeouted")
        from states.Candidate import Candidate
        self.node.manuallySwitchState(Candidate())

