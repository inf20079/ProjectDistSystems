from middleware.types.MessageTypes import AddEntryMessage, ResponseVoteMessage
from states.State import State


class Voter(State):

    def __init__(self):
        self.lastVote = None

    def onVoteRequestReceived(self, message):
        print("onVoteRequestReceived")

        if (self.lastVote is None and
                message is AddEntryMessage and
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
            vote=vote
        )
        self.node.sendResponseMessage(voteResponse)
