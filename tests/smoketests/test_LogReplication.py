from time import sleep

from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestLogReplication(SmokeTest):

    def test_LogReplication(self):
        """Start 3 nodes in the cluster, run the simulation with one client, verify that the commands are replicated to all
        followers"""
        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(1)
        sleep(5)  # Let client send a few messages

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: len(self.nodes[0].log) > 0,
            maxDuration=maxDuration,
            onFailedText=f"Leader did not append an action to its log after {maxDuration} seconds."
        )

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: self.checkIfLogsAreEqual(1, 2) and self.checkIfLogsAreEqual(1, 3),
            maxDuration=maxDuration,
            onFailedText=f"Followers did not replicate the log after {maxDuration} seconds."
        )

    def test_Restart_ReplicateLog(self):
        """Start 3 Nodes in the cluster and simulate the failure of a follower.
        Run the simulation with one client. After some time, restart the node and
        verify that it copies and applies all logs"""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.deleteNode(3)
        sleep(1)
        self.createAndStartClient(1)
        sleep(5)
        self.startNode(3, Follower)

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: self.checkIfLogsAreEqual(1, 3),
            maxDuration=maxDuration,
            onFailedText=f"Follower did not replicate the log after {maxDuration} seconds."
        )

    def test_Restart_ReplicateFromFileAndLog(self):
        """Start 3 Nodes in the cluster and run the simulation with one client.
        After some time, simulate the failure of a follower.
        After some time, restart the node and verify that it (i) restores
        all logs and the TrafficAreaNode{nodeID} file and (ii) retrieves all logs
        it has not seen yet from the Leader and applies them to its state machine"""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)
        self.createAndStartClient(1)
        sleep(5)
        self.deleteNode(3)
        sleep(5)
        self.startNode(3, Follower)

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: self.checkIfLogsAreEqual(1, 3),
            maxDuration=maxDuration,
            onFailedText=f"Follower did not replicate the log after {maxDuration} seconds."
        )

