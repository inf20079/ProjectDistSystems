from middleware.types.MessageTypes import ClientRequestMessage
from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestLogReplication(SmokeTest):

    def test_LogReplication(self):
        """Start 3 nodes in the cluster, write a command to the leader, verify that the command is replicated to all
        followers"""
        self.createNodes(types=[Leader, Follower, Follower])

        message = ClientRequestMessage(blablabla=1)
        self.nodes[0].state.onClientRequestReceived(message)

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: len(self.nodes[0].log) > 0,
            maxDuration=maxDuration,
            onFailedText=f"Leader did not append an action to its log after {maxDuration} seconds."
        )

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: len(self.nodes[1].log) > 0 and len(self.nodes[2].log) > 0,
            maxDuration=maxDuration,
            onFailedText=f"Followers did not replicate the log after {maxDuration} seconds."
        )