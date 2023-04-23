from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage
from states.Follower import Follower
from states.Leader import Leader
from states.Voter import Voter


class Candidate(Voter):

    def setNode(self, node):
        super().setNode(node)
        self.votedFor = None
        self.votesReceived = 0
        self.startElection()

    def onVoteRequestReceived(self, message):
        print("(Candidate) onVoteRequestReceived")

        # Check if the message's term is greater than the candidate's current term
        if message.term > self.node.currentTerm:
            self.onMessageWithGreaterTerm(message)
            self.votedFor = None
            return Follower(), None

        # If the candidate has already voted for someone else in this term, reject the vote
        if self.votedFor is not None and self.votedFor != message.senderID:
            return self.generateVoteResponse(message, False)

        # If the candidate's log is at least as up-to-date as the voter's log, reject the vote
        if (len(self.node.log) == 0 and message.lastLogIndex == -1) or \
                len(self.node.log) > 0 and \
                (
                    self.node.log[-1].term > message.lastLogTerm or
                    (self.node.log[-1].term == message.lastLogTerm and len(self.node.log) - 1 > message.lastLogIndex)
                ):
            return self.generateVoteResponse(message, False)

        # Grant the vote and reset the election timeout
        self.votedFor = message.senderID
        print(message.senderID)
        self.resetElectionTimeout()

        return self, self.generateVoteResponse(message, True)

    def generateVoteResponse(self, message, vote: bool):
        return self, ResponseVoteMessage(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=self.node.currentTerm,
            voteGranted=vote
        )

    def onVoteResponseReceived(self, message: ResponseVoteMessage):
        print("(Candidate) onVoteResponseReceived")

        # Check if the message's term is greater than the candidate's current term
        if message.term > self.node.currentTerm:
            self.onMessageWithGreaterTerm(message)
            return Follower(), None

        # If the vote was granted, increment the vote count and check if the candidate
        # has received votes from a majority of the cluster
        if message.voteGranted:
            self.votesReceived += 1
            if self.votesReceived > len(self.node.peers) // 2:
                return Leader(), None

        return self, None

    def startElection(self):
        """When a Candidate starts an election, it increments the current term, votes for itself,
        and sends RequestVoteRequest messages to all other nodes in the cluster.
        It also resets the election timeout."""

        # Reset the election timeout
        self.resetElectionTimeout()

        # Increment the current term and vote for self
        self.node.currentTerm += 1
        self.votedFor = self.node.id
        self.votesReceived = 1

        # Send RequestVoteMessage messages to all other nodes in the cluster
        requestVoteMessage = RequestVoteMessage(
            senderID=self.node.id,
            receiverID=-1,  # ToDo: set in Broadcast. Or leave blank
            term=self.node.currentTerm,
            lastLogIndex=len(self.node.log) - 1,
            lastLogTerm=self.node.log[-1].term if len(self.node.log) > 0 else -1
        )

        return self, requestVoteMessage
