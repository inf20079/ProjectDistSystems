import configparser
import os
import threading
import unittest
from time import sleep
from typing import List

from client.Client import Client
from middleware.types.MessageTypes import Member, Coordinate
from node.Node import Node
from node.RecurringProcedure import RecurringProcedure
from states.Follower import Follower
from states.Leader import Leader


class SmokeTest(unittest.TestCase):

    def setUp(self) -> None:
        RecurringProcedure.TIMEOUT_SCALE = 20

        dir = os.getcwd() + os.sep + "temp"
        if os.path.exists(dir):
            filelist = [f for f in os.listdir(dir) if f.endswith(".pkl")]
            for f in filelist:
                os.remove(os.path.join(dir, f))

    def createNodes(self, types):
        nodeCount = len(types)
        self.nodes: List[Node] = []

        self.config = configparser.ConfigParser()
        self.config.read(os.getcwd() + os.sep + "/../../config/cluster.cfg")

        self.broadcastPort = self.config.get("cluster", "broadcastPort")

        memberStr = self.config.get('cluster', 'memberList', fallback='').split(',')
        self.members = [Member(id=int(id), port=int(self.config.get(str(id), "port")), host=self.config.get(str(id), "ip"))
                   for id in memberStr]

        for i in range(nodeCount):
            nodeID = i + 1
            self.startNode(nodeID, types[i])

        self.nodesLoopRunning = True
        threading.Thread(
            target=self.nodesLoop
        ).start()

    def startNode(self, nodeID, type):
        ip = self.config.get(str(nodeID), "ip")
        port = self.config.get(str(nodeID), "port")
        peers = [member for member in self.members if member.id != nodeID]
        node = Node(stateClass=type, id=nodeID, ipAddress=str(ip), unicastPort=int(port),
                    broadcastPort=int(self.broadcastPort), peers=peers)
        self.nodes.append(node)

    def deleteNode(self, nodeID):
        node = self.getNodeByID(nodeID)
        node.shutdown()
        self.nodes.remove(node)
        del node

    def nodesLoop(self):
        while self.nodesLoopRunning:
            for node in self.nodes:
                node.pollMessages()

    def getNodeByID(self, nodeID):
        return [node for node in self.nodes if node.id == nodeID][0]

    def createAndStartClient(self, clientCount: int, destinations: [Coordinate] = None):
        if not hasattr(self, "clients"):
            self.clients = []
        for i in range(0, clientCount):
            client = Client(destinations[i] if destinations and i < len(destinations) else Coordinate(15, 15),
                            [(node.ipAddress, node.unicastPort) for node in self.nodes],
                            "localhost", 18011 + i,
                            1000, 1000, i)
            client.start()
            self.clients.append(client)

    def tearDown(self):
        self.nodesLoopRunning = False
        for node in self.nodes:
            node.shutdown()

        if hasattr(self, "clients"):
            for client in self.clients:
                client.shutdown()

    def checkForDuration(self, passCondition, maxDuration, onFailedText):
        currDuration = 0
        while not passCondition():
            sleep(0.5)
            currDuration += 1
            if currDuration >= maxDuration:
                self.fail(onFailedText)

    def checkIfLogsAreEqual(self, nodeID_A, nodeID_B):
        """Log Matching Property of Raft"""
        node_A = self.getNodeByID(nodeID_A)
        node_B = self.getNodeByID(nodeID_B)

        return self.checkIfLogsAreEqual_Logs(node_A.log, node_B.log)

    def checkIfLogsAreEqual_Logs(self, log_A, log_B):
        if len(log_A) != len(log_B):
            return False

        if log_A[-1].term != log_B[-1].term:
            return False

        return True

