from middleware.types.MessageTypes import AppendEntriesRequest, AppendEntriesResponse
from states.Voter import Voter


class Follower(Voter):

    def __init__(self):
        Voter.__init__(self)
        self.leaderID = None

    def onAppendEntries(self, message: AppendEntriesRequest):
        print("(Follower) onAddEntries")

        self.resetElectionTimeout()

        # Reply false if message.term < currentTerm
        if message.term < self.node.currentTerm:
            response = self.generateAppendEntriesResponse(message, False)
            return self, response

        self.node.currentTerm = message.term
        self.leaderID = message.senderID

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

    def generateAppendEntriesResponse(self, message, success):
        return AppendEntriesResponse(
            senderID=self.node.id,
            receiverID=message.senderID,
            term=self.node.currentTerm,
            success=success
        )
