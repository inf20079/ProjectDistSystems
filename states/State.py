import time
import random

class State:

    def setNode(self, node):
        self.node = node

    def onMessage(self, message):
        """Called when a message is received.
        Calls an appropriate other method as a reaction."""

    def onLeaderTimeout(self, message):
        """Called when leader timeout was reached"""

    def onAddEntryReceived(self, message):
        """Called when a request to add an entry was received"""

    def nextTimeout(self):
        self.currentTime = time.time()
        return self.currentTime + random.randrange(self.timeout, 2 * self.timeout)