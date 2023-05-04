from time import sleep

from middleware.types.MessageTypes import Coordinate
from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestStateMachineReplication(SmokeTest):

    def test_StateMachineReplication(self):
        """Start a cluster with 3 nodes. Run the simulation for some time with one client.
        Verify that all StateMachines produce the same results by checking that all TrafficAreas
        are the same"""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(1, destinations=[Coordinate(3, 3)])
        sleep(5)  # Let simulation run

        # First of all, client must reach destination. Otherwise, TrafficAreas might not match, as Follower's only
        # update them after the next heartbeat, when a new commitIndex is sent.
        maxDuration = 30
        self.checkForDuration(
            passCondition=lambda: self.clients[0].destinationReached,
            maxDuration=maxDuration,
            onFailedText=f"Client did not reach destination after {maxDuration} seconds."
        )

        maxDuration = 10
        self.checkForDuration(
            passCondition=lambda: self.getNodeByID(1).trafficControlLogic.trafficArea.getArea() == self.getNodeByID(2).trafficControlLogic.trafficArea.getArea(),
            maxDuration=maxDuration,
            onFailedText=f"TestAreas were not the same after {maxDuration} seconds."
        )
