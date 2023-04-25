import random
import threading
import time

from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage
from node.RecurringProcedure import RecurringProcedure
from states.State import State


class Voter(State):

    def __init__(self):
        self.votedFor = None
        self.electionTimeout = 3  # random.randrange(150, 300) / 1000
        self.electionActive = True
        self.recurringProcedure = RecurringProcedure(self.electionTimeout, self.onElectionTimeouted)

    def setNode(self, node):
        super().setNode(node)
        self.recurringProcedure.start()

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        print(f"[{self.node.id}](Voter) onVoteRequestReceived")

        # If the voter has already voted for someone else in this term, reject the vote
        if self.votedFor is not None and self.votedFor != message.senderID:
            print(f"[{self.node.id}](Voter) onVoteRequestReceived: candidate has already voted")
            return self, self.generateVoteResponseMessage(message, False)

        # votedFor is None or message.senderID

        # If the candidate's log is less up-to-date as the voter's log, reject the vote
        if message.lastLogIndex < self.node.lastLogIndex():
            print(f"[{self.node.id}](Voter) onVoteRequestReceived: candidate's log less up-to-date as voter's log")
            return self, self.generateVoteResponseMessage(message, False)

        self.votedFor = message.senderID
        self.recurringProcedure.resetTimeout()

        return self, self.generateVoteResponseMessage(message, True)

    def onElectionTimeouted(self):
        """Must be implemented in children"""

    def shutdown(self):
        if self.node is not None:
            print(f"[{self.node.id}](Voter) shutdown")
        self.recurringProcedure.shutdown()
