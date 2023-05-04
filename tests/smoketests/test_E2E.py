from time import sleep

from middleware.types.MessageTypes import Coordinate
from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestE2E(SmokeTest):

    def test_OneClient(self):
        """Start 3 nodes in the cluster and run the simulation with one client.
        Check, whether client finds its way to his destination"""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(1, destinations=[Coordinate(5, 5)])

        maxDuration = 30
        self.checkForDuration(
            passCondition=lambda: self.clients[0].destinationReached,
            maxDuration=maxDuration,
            onFailedText=f"Client did not reach destination after {maxDuration} seconds."
        )

    def test_TwoClients(self):
        """Start 3 nodes in the cluster and run the simulation with two clients.
        Check, whether all clients reach their destination."""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(2, destinations=[Coordinate(3, 5), Coordinate(5, 3)])

        maxDuration = 300
        self.checkForDuration(
            passCondition=lambda: all(client.destinationReached for client in self.clients),
            maxDuration=maxDuration,
            onFailedText=f"Client did not reach destination after {maxDuration} seconds."
        )

    def test_FiveClients(self):
        """Start 3 nodes in the cluster and run the simulation with five clients.
                Check, whether all clients reach their destination."""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(5, destinations=[Coordinate(5, 5), Coordinate(5, 5), Coordinate(6, 6),
                                                   Coordinate(7, 4), Coordinate(8, 10)])

        maxDuration = 300
        self.checkForDuration(
            passCondition=lambda: all(client.destinationReached for client in self.clients),
            maxDuration=maxDuration,
            onFailedText=f"Client did not reach destination after {maxDuration} seconds."
        )

    def test_TenClients(self):
        """Start 3 nodes in the cluster and run the simulation with ten clients.
        Check, whether all clients reach their destination."""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(10, destinations=[Coordinate(5, 5), Coordinate(5, 5), Coordinate(6, 6),
                                                    Coordinate(7, 4), Coordinate(8, 10), Coordinate(17, 3),
                                                    Coordinate(2, 3), Coordinate(6, 8), Coordinate(7, 7),
                                                    Coordinate(8, 5)])

        maxDuration = 300
        self.checkForDuration(
            passCondition=lambda: all(client.destinationReached for client in self.clients),
            maxDuration=maxDuration,
            onFailedText=f"Client did not reach destination after {maxDuration} seconds."
        )
