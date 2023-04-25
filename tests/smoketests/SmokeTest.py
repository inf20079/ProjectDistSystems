import configparser
import os
import threading
import unittest
from time import sleep
from typing import List

from middleware.types.MessageTypes import Member
from node.Node import Node
from node.RecurringProcedure import RecurringProcedure
from states.Follower import Follower


class SmokeTest(unittest.TestCase):

    def setUp(self) -> None:
        RecurringProcedure.TIMEOUT_SCALE = 10

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
            self.createSingleNode(nodeID, types[i])

        self.nodesLoopRunning = True
        threading.Thread(
            target=self.nodesLoop
        ).start()

    def createSingleNode(self, nodeID, type):
        ip = self.config.get(str(nodeID), "ip")
        port = self.config.get(str(nodeID), "port")
        peers = [member for member in self.members if member.id != nodeID]
        node = Node(stateClass=type, id=nodeID, ipAddress=str(ip), unicastPort=int(port),
                    broadcastPort=int(self.broadcastPort), peers=peers)
        self.nodes.append(node)

    def nodesLoop(self):
        while self.nodesLoopRunning:
            for node in self.nodes:
                node.pollMessages()

    def tearDown(self):
        self.nodesLoopRunning = False
        for node in self.nodes:
            node.shutdown()

    def checkForDuration(self, passCondition, maxDuration, onFailedText):
        currDuration = 0
        while not passCondition():
            sleep(1)
            currDuration += 1
            if currDuration >= maxDuration:
                self.fail(onFailedText)
