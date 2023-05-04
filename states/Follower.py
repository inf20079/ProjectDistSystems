from middleware.types.MessageTypes import AppendEntriesRequest, NavigationRequest, Member, NavigationResponse
from states.Voter import Voter


class Follower(Voter):

    def __init__(self, node):
        super().__init__(node)
        self.leader = None

    def onAppendEntries(self, message: AppendEntriesRequest):
        self.leader = self.node.getIpByID(message.senderID)
        self.recurringProcedure.resetTimeout()
        return super().onAppendEntries(message)

    def onClientRequestReceived(self, message: NavigationRequest):
        # print(f"[{self.node.id}](Follower) onClientRequestReceived")
        if self.leader is not None:
            response = NavigationResponse(message.clientId, None, self.leader)
            self.node.sendMessageUnicast(response, message.clientHost, message.clientPort)
        else:
            response = NavigationResponse(message.clientId, None, None)
            self.node.sendMessageUnicast(response, message.clientHost, message.clientPort)

    def onElectionTimeouted(self):
        # print(f"[{self.node.id}](Follower) onElectionTimeouted")
        from states.Candidate import Candidate
        self.node.manuallySwitchState(Candidate)

