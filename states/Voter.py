import random
import threading
import time

from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage, NavigationRequest
from node.RecurringProcedure import RecurringProcedure
from states.State import State


class Voter(State):

    def __init__(self, node):
        super().__init__(node)
        self.votedFor = {}  # dict: term -> candidate

        electionTimeout = random.randrange(300, 600) / 1000  # Raft usually uses (150, 300), but our network is
        # pretty slow, and we don't want to timeout as easily
        self.recurringProcedure = RecurringProcedure(electionTimeout, self.onElectionTimeouted)

        self.recurringProcedure.start()

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        # print(f"[{self.node.id}](Voter) onVoteRequestReceived from candidate {message.senderID}")

        # If the voter has already voted for someone else in this term, reject the vote
        if message.term in self.votedFor.keys() and self.votedFor[message.term] != message.senderID:
            # print(f"[{self.node.id}](Voter) onVoteRequestReceived: voter has already voted")
            return self.__class__, self.generateVoteResponseMessage(message, False)

        # votedFor is None or message.senderID

        # If the candidate's log is less up-to-date as the voter's log, reject the vote
        if message.lastLogIndex < self.node.lastLogIndex():
            # print(f"[{self.node.id}](Voter) onVoteRequestReceived: candidate's log less up-to-date as voter's log")
            return self.__class__, self.generateVoteResponseMessage(message, False)

        self.votedFor[message.term] = message.senderID
        self.recurringProcedure.resetTimeout()

        # print(f"[{self.node.id}](Voter) onVoteRequestReceived: voting for candidate")

        return self.__class__, self.generateVoteResponseMessage(message, True)

    def onElectionTimeouted(self):
        """Must be implemented in children"""

    def shutdown(self):
        # print(f"[{self.node.id}](Voter) shutdown")
        self.recurringProcedure.shutdown()
