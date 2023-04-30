from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestLeaderElection(SmokeTest):

    def test_startToLeader(self):
        """Start 3 nodes in the cluster (all Followers) and verify that only one node becomes leader"""
        self.createNodes(types=[Follower, Follower, Follower])

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: sum(isinstance(node.state, Leader) for node in self.nodes) == 1,
            maxDuration=maxDuration,
            onFailedText=f"No Leader after {maxDuration} seconds."
        )

    def test_onLeaderKilled(self):
        """Start 3 nodes in the cluster (one Leader, two Followers), kill the current leader and verify that another
        node becomes leader"""

        self.createNodes(types=[Leader, Follower, Follower])
        if sum(isinstance(node.state, Leader) for node in self.nodes) != 1:
            self.fail("CANNOT START TEST: LEADER COUNT != 1")

        self.nodes[0].shutdown()
        del self.nodes[0]

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: sum(isinstance(node.state, Leader) for node in self.nodes) == 1,
            maxDuration=maxDuration,
            onFailedText=f"No node became Leader after {maxDuration} seconds."
        )

    def test_onNodeRestart(self):
        """Start two nodes in the cluster (both Follower), wait for one to become Leader in a new term, restart the
        third node (Leader) and verify that it becomes a Follower"""

        self.createNodes(types=[Follower, Follower])

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: sum(isinstance(node.state, Leader) for node in self.nodes) == 1,
            maxDuration=maxDuration,
            onFailedText=f"No node became Leader after {maxDuration} seconds."
        )

        self.createSingleNode(nodeID=3, type=Leader)

        maxDuration = 20
        self.checkForDuration(
            passCondition=lambda: self.nodes[2].id == 3 and isinstance(self.nodes[2].state, Follower),
            maxDuration=maxDuration,
            onFailedText=f"Restarted Leader didn't become Follower after {maxDuration} seconds."
        )
