import time
import random
from middleware.types.MessageTypes import *


class State:

    def __init__(self, node):
        self.node = node

    def onRaftMessage(self, message: Message):
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
            self.node.currentTerm = message.term  # Update here already, because we might need it in the subsequent
            # actions
            if isinstance(self, Candidate):
                self.shutdown()  # Already stop election timeout here, because it is running in a separate thread and
                # might execute between here and the actual state-transition

        stateClass, response = self.__class__, None

        if isinstance(message, AppendEntriesRequest):
            stateClass, response = self.onAppendEntries(message)
        elif isinstance(message, AppendEntriesResponse):
            if isinstance(self, Leader):
                stateClass, response = self.onResponseReceived(message)
            else:
                print(f"[{self.node.id}](State) onMessage / AppendEntriesResponse: instance not a leader")
        elif isinstance(message, RequestVoteMessage):
            stateClass, response = self.onVoteRequestReceived(message)
        elif isinstance(message, ResponseVoteMessage):
            if isinstance(self, Candidate):
                stateClass, response = self.onVoteResponseReceived(message)
            else:
                print(f"[{self.node.id}](State) onMessage: instance not a candidate")

        # If RPC request or response contains term T > currentTerm:
        # convert to follower
        if message.term > prevCurrentTerm:
            print(f"[{self.node.id}](State) onMessage: message.term > prevCurrentTerm")
            if not isinstance(self, Follower):
                stateClass = Follower

        if response is not None:
            response.term = self.node.currentTerm

        return stateClass, response

    def onAppendEntries(self, message: AppendEntriesRequest):
        print(f"[{self.node.id}](State) onAppendEntries")

        print(f"[{self.node.id}](State) onAppendEntries: {message.term=}")
        print(f"[{self.node.id}](State) onAppendEntries: {self.node.currentTerm=}")

        # Reply false if message.term < currentTerm
        if message.term < self.node.currentTerm:
            print(f"[{self.node.id}](State) onAppendEntries: message.term < self.node.currentTerm")
            return self.__class__, self.generateAppendEntriesResponse(message, False)

        self.node.currentTerm = message.term

        # Reply false if log doesn't contain an entry at prevLogIndex whose term matches prevLogTerm
        if message.prevLogIndex >= 0:
            prevLog = self.node.log[message.prevLogIndex]
            if prevLog.term != message.prevLogTerm:
                # The previous log entry doesn't match, so send a
                # failure response indicating the mismatch
                print(f"[{self.node.id}](State) onAppendEntries: The previous log entry doesn't match")
                return self.__class__, self.generateAppendEntriesResponse(message, False)

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
        self.node.log += message.entries[j:]

        print(f"[{self.node.id}](State) onAppendEntries: {self.node.log=}")

        # If leaderCommit > commitIndex, set commitIndex =
        # min(leaderCommit, index of last new entry)
        if message.commitIndex > self.node.commitIndex:
            self.node.commitIndex = min(
                message.commitIndex, self.node.lastLogIndex()
            )

        # Send a success message
        print(f"[{self.node.id}](State) onAppendEntries: Success")
        return self.__class__, self.generateAppendEntriesResponse(message, True)

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
        a = ResponseVoteMessage(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=message.term,
            voteGranted=vote
        )
        return a

    def shutdown(self):
        """To be overriden"""

