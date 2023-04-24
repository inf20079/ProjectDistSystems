from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage, AppendEntriesRequest
from states.Follower import Follower
from states.Leader import Leader
from states.Voter import Voter


class Candidate(Voter):

    def setNode(self, node):
        print(f"[{node.id}](Candidate) setNode")
        super().setNode(node)

        if len(self.node.peers) == 0:
            node.manuallySwitchState(Leader())
            return

        self.votesReceived = 0
        self.startElection()

    def onAppendEntries(self, message: AppendEntriesRequest):
        state, response = super().onAppendEntries(message)
        return Follower(), response

    def onVoteResponseReceived(self, message: ResponseVoteMessage):
        print(f"[{self.node.id}](Candidate) onVoteResponseReceived")

        print(self.votesReceived)

        # Check if the message's term is greater than the candidate's current term
        if message.term > self.node.currentTerm:
            print(f"[{self.node.id}](Candidate) onVoteResponseReceived: higher term")
            return Follower(), None

        # If the vote was granted, increment the vote count and check if the candidate
        # has received votes from a majority of the cluster
        if message.voteGranted:
            self.votesReceived += 1
            print(f"[{self.node.id}](Candidate) onVoteResponseReceived: vote granted")
            if self.votesReceived > len(self.node.peers) // 2:
                print(f"[{self.node.id}](Candidate) onVoteResponseReceived: majority votes")
                return Leader(), None
            return self, None

        print(f"[{self.node.id}](Candidate) onVoteResponseReceived: vote not granted")
        return self, None

    def onElectionTimeouted(self):
        # print(f"[{self.node.id}](Candidate) onElectionTimeouted")
        self.startElection()

    def startElection(self):
        """When a Candidate starts an election, it increments the current term, votes for itself,
        and sends RequestVoteRequest messages to all other nodes in the cluster.
        It also resets the election timeout."""

        print(f"[{self.node.id}](Candidate) startElection")

        # Reset the election timeout
        self.recurringProcedure.resetTimeout()

        # Increment the current term and vote for self
        self.node.currentTerm += 1
        self.votedFor = self.node.id
        self.votesReceived = 1

        # Send RequestVoteMessage messages to all other nodes in the cluster
        requestVoteMessage = RequestVoteMessage(
            senderID=self.node.id,
            receiverID=-1,
            term=self.node.currentTerm,
            lastLogIndex=len(self.node.log) - 1,
            lastLogTerm=self.node.lastLogTerm()
        )

        self.node.sendMessageBroadcast(requestVoteMessage)

