import random

from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage
from states.State import State


class Voter(State):

    def __init__(self):
        self.votedFor = None
        self.currElectionTimeout = 0
        self.maxElectionTimeout = random.randrange(150, 300)  # in milliseconds

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        print("(Voter) onVoteRequestReceived")

        # If the voter has already voted for someone else in this term, reject the vote
        if self.votedFor is not None and self.votedFor != message.senderID:
            print("(Voter) onVoteRequestReceived: candidate has already voted")
            return self, self.generateVoteResponseMessage(message, False)

        # votedFor is None or message.senderID

        # If the candidate's log is less up-to-date as the voter's log, reject the vote
        if message.lastLogIndex < self.node.lastLogIndex():
            print("(Voter) onVoteRequestReceived: candidate's log less up-to-date as voter's log")
            return self, self.generateVoteResponseMessage(message, False)

        self.votedFor = message.senderID
        self.resetElectionTimeout()

        return self, self.generateVoteResponseMessage(message, True)

    def generateVoteResponseMessage(self, message, vote: bool):
        return ResponseVoteMessage(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=message.term,
            voteGranted=vote
        )

    def resetElectionTimeout(self):
        self.currElectionTimeout = 0
