import configparser
import os
import threading
import unittest
from time import sleep
from typing import List

from middleware.types.MessageTypes import Member
from node.Node import Node
from states.Follower import Follower


class TestLeaderElection(unittest.TestCase):

    def setUp(self):
        nodeCount = 3
        self.nodes: List[Node] = []

        config = configparser.ConfigParser()
        config.read(os.getcwd() + os.sep + "/../../config/cluster.cfg")

        print(config)

        broadcastPort = config.get("cluster", "broadcastPort")

        memberStr = config.get('cluster', 'memberList', fallback='').split(',')
        members = [Member(id=int(id), port=int(config.get(str(id), "port")), host=config.get(str(id), "ip")) for id in
                   memberStr]
        for i in range(nodeCount):
            nodeID = i + 1
            ip = config.get(str(nodeID), "ip")
            port = config.get(str(nodeID), "port")
            peers = [member for member in members if member.id != nodeID]
            node = Node(stateClass=Follower, id=nodeID, ipAddress=str(ip), unicastPort=int(port),
                        broadcastPort=int(broadcastPort), peers=peers)
            self.nodes.append(node)

        self.nodesLoopRunning = True
        threading.Thread(
            self.nodesLoop()
        ).start()

    def nodesLoop(self):
        while self.nodesLoopRunning:
            for node in self.nodes:
                node.pollMessages()
            sleep(0.0001)

    def tearDown(self):
        self.nodesLoopRunning = False
        for node in self.nodes:
            node.shutdown()

    def test_LeaderElection(self):
        for i in range(60):
            for node in self.nodes:
                print(node.__class__)
            sleep(1)
        print("nah")
