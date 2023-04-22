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

        if (message.term > self.node.currentTerm):
            self.node.currentTerm = message.term
        elif (message.term < self.node.currentTerm):
            # ToDo: Tell the sender that they're behind
            pass

        if isinstance(message, AddEntryMessage):
            if isinstance(self, Follower):
                return self.onAddEntries(message)
            print("instance not a follower")
        elif isinstance(message, RequestVoteMessage):
            if isinstance(self, Voter):
                return self.onVoteRequestReceived(message)
            print("instance not a voter")
        elif isinstance(message, ResponseVoteMessage):
            if isinstance(self, Candidate):
                return self.onVoteResponseReceived(message)
            print("instance not a candidate")
        elif isinstance(self, AddEntriesResponse):
            if isinstance(self, Leader):
                return self.onResponseReceived(message)
            print("instance not a leader")

        print("something went wrong")
        return self, None





    def onLeaderTimeout(self, message):
        """Called when leader timeout was reached"""

    def onAddEntryReceived(self, message):
        """Called when a request to add an entry was received"""

    def nextTimeout(self):
        self.currentTime = time.time()
        return self.currentTime + random.randrange(self.timeout, 2 * self.timeout)