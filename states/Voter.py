import random
import threading
import time

from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage
from states.State import State


class Voter(State):

    def __init__(self):
        self.votedFor = None
        self.electionTimeout = random.randrange(150, 300) / 100  # in milliseconds
        self.electionActive = True

    def setNode(self, node):
        super().setNode(node)
        self.resetElectionTimeout()
        threading.Thread(
            target=self.watchElectionTimeout
        ).start()
        print("(Voter) setNode done")

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

    def watchElectionTimeout(self):
        while self.electionActive:
            while time.time() >= self.nextElectionTimeout and self.electionActive:  # wait for reset
                time.sleep(0.01)
            while time.time() < self.nextElectionTimeout and self.electionActive:  # count down
                time.sleep(0.01)
            self.onElectionTimeouted()

    def onElectionTimeouted(self):
        """Must be implemented in children"""

    def resetElectionTimeout(self):
        # print("resetElectionTimeout")
        self.nextElectionTimeout = time.time() + self.electionTimeout

    def shutdown(self):
        print("Voter shutdown")
        self.electionActive = False
