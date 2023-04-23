import time
import random
from middleware.types.MessageTypes import *


class State:

    def setNode(self, node):
        self.node = node

    def onMessage(self, message: Message):
        """Called when a message is received.
        Calls an appropriate other method as a reaction."""

        # Imports here: Would cause circular import at head of module
        from states.Candidate import Candidate
        from states.Follower import Follower
        from states.Leader import Leader
        from states.Voter import Voter

        prevCurrentTerm = self.node.currentTerm
        # If RPC request or response contains term T > currentTerm:
        # set currentTerm = T
        if message.term > self.node.currentTerm:
            self.node.currentTerm = message.term

        state, response = self, None

        if isinstance(message, AppendEntriesRequest):
            state, response = self.onAppendEntries(message)
        elif isinstance(message, AppendEntriesResponse):
            if isinstance(self, Leader):
                state, response = self.onResponseReceived(message)
            else:
                print("instance not a leader")
        elif isinstance(message, RequestVoteMessage):
            state, response = self.onVoteRequestReceived(message)
        elif isinstance(message, ResponseVoteMessage):
            if isinstance(self, Candidate):
                state, response = self.onVoteResponseReceived(message)
            else:
                print("instance not a candidate")

        # If RPC request or response contains term T > currentTerm:
        # convert to follower
        if message.term > prevCurrentTerm:
            if state is self and not isinstance(self, Follower):
                state = Follower()

        return state, response

    def onAppendEntries(self, message: AppendEntriesRequest):
        """To be overriden by children"""

        print("(State) onAddEntries")

        # Reply false if message.term < currentTerm
        if message.term < self.node.currentTerm:
            response = self.generateAppendEntriesResponse(message, False)
            return self, response

        self.node.currentTerm = message.term

        # Reply false if log doesn't contain an entry at prevLogIndex whose term matches prevLogTerm
        if message.prevLogIndex >= 0:
            prevLog = self.node.log[message.prevLogIndex]
            if prevLog.term != message.prevLogTerm:
                # The previous log entry doesn't match, so send a
                # failure response indicating the mismatch
                response = self.generateAppendEntriesResponse(message, False)
                return self, response

        # If an existing entry conflicts with a new one (same index but different terms),
        # delete the existing entry and all that follow it
        i = message.prevLogIndex + 1
        j = 0
        while i < len(self.node.log) and j < len(message.entries):
            if self.node.log[i].term != message.entries[j].term:
                del self.node.log[i:]
                break
            i += 1
            j += 1

        # Append any new entries not already in the log
        self.node.log.append(message.entries[j:])

        # If leaderCommit > commitIndex, set commitIndex =
        # min(leaderCommit, index of last new entry)
        if message.commitIndex > self.node.commitIndex:
            self.node.commitIndex = min(
                message.commitIndex, len(self.node.log) - 1
            )

        # Send a success message
        response = self.generateAppendEntriesResponse(message, True)
        return self, response

    def onVoteRequestReceived(self, message: RequestVoteMessage):
        """To be implemented by Voter and Leader"""

    def generateAppendEntriesResponse(self, message, success):
        return AppendEntriesResponse(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=self.node.currentTerm,
            success=success
        )

    def generateVoteResponseMessage(self, message, vote: bool):
        return ResponseVoteMessage(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=message.term,
            voteGranted=vote
        )

    def nextTimeout(self):
        self.currentTime = time.time()
        return self.currentTime + random.randrange(self.timeout, 2 * self.timeout)
