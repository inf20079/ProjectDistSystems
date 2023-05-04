from time import sleep

from middleware.types.MessageTypes import Coordinate
from states.Follower import Follower
from states.Leader import Leader
from tests.smoketests.SmokeTest import SmokeTest


class TestSystemFailure(SmokeTest):

    def test_SystemFailure(self):
        """Start 3 nodes in the cluster. Run the simulation with one client. After some time,
        simulate a failure of all three nodes. Restart them and check that the
        TrafficAreas are still the same"""

        self.createNodes(types=[Leader, Follower, Follower])

        sleep(1)  # Wait a short time until cluster has started
        self.createAndStartClient(1, destinations=[Coordinate(500, 500)])
        sleep(10)  # Let the simulation run

        trafficAreasBefore = [node.trafficControlLogic.trafficArea.getArea() for node in self.nodes]
        logsBefore = [node.log for node in self.nodes]

        self.deleteNode(1)
        self.deleteNode(2)
        self.deleteNode(3)

        sleep(2)

        self.startNode(1, Follower)
        self.startNode(2, Follower)
        self.startNode(3, Follower)

        trafficAreasAfter = [node.trafficControlLogic.trafficArea.getArea() for node in self.nodes]
        logsAfter = [node.log for node in self.nodes]

        for i in range(0, len(self.nodes)):
            self.assertEqual(trafficAreasBefore[i], trafficAreasAfter[i])
            self.checkIfLogsAreEqual_Logs(logsBefore[i], logsAfter[i])

