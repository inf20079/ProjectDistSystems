from time import sleep

from client.Client import Client
from middleware.types.MessageTypes import Coordinate
from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestLogReplication(SmokeTest):

    def test_LogReplication(self):
        """Start 3 nodes in the cluster, write a command to the leader, verify that the command is replicated to all
        followers"""
        self.createNodes(types=[Leader, Follower, Follower])

        sleep(5)

        client = Client(Coordinate(5, 5), [(self.nodes[0].ipAddress, self.nodes[0].unicastPort)], "localhost", 14009, 100, 100, 0)
        client.start()

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