from middleware.types.MessageTypes import AppendEntriesRequest, ResponseVoteMessage, RequestVoteMessage
from states.State import State


class Voter(State):

    def __init__(self):
        self.lastVote = None
        self.electionTimeout = 0

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        print("onVoteRequestReceived")

        if (self.lastVote is None and
                message is AppendEntriesRequest and
                message.lastLogIndex >= self.node.lastLogIndex):
            self.lastVote = message.senderID
            self.sendVoteResponseMessage(message, True)
        else:
            self.sendVoteResponseMessage(message, False)

        return self, None

    def sendVoteResponseMessage(self, message, vote: bool):
        voteResponse = ResponseVoteMessage(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=message.term,
            voteGranted=vote
        )
        self.node.sendResponseMessage(voteResponse)


    def resetElectionTimeout(self):
        # ToDo
        pass
