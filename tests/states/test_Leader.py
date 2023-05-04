import unittest

from node.Node import Node
from states.Leader import Leader
from middleware.types.MessageTypes import AppendEntriesResponse, LogEntry, NavigationRequest, Coordinate


class TestLeader(unittest.TestCase):
    def setUp(self):
        self.leaderNode = Node(0, Leader, peers=[1, 2],
                               log=[LogEntry(0, NavigationRequest(
                                    clientId=0,
                                    clientHost="localhost",
                                    clientPort=18011,
                                    currentPosition=Coordinate(None, None),
                                    destination=Coordinate(2, 2)
                               ))])
        self.leader = self.leaderNode.state

    def tearDown(self):
        self.leaderNode.shutdown()

    def test_onAppendEntriesResponseReceived_Successful(self):
        message = AppendEntriesResponse(
            senderID=1,
            receiverID=0,
            term=1,
            success=True
        )

        stateClass, response = self.leader.onAppendEntriesResponseReceived(message)

        self.assertEqual(stateClass, Leader)
        self.assertIsNone(response)
        self.assertEqual(1, self.leader.nextIndex[1])

    def test_onAppendEntriesResponseReceived_Failed(self):
        message = AppendEntriesResponse(
            senderID=1,
            receiverID=0,
            term=0,
            success=False
        )

        stateClass, response = self.leader.onAppendEntriesResponseReceived(message)

        self.assertEqual(stateClass, Leader)
        self.assertIsNotNone(response)
        self.assertEqual(0, self.leader.nextIndex[1])  # decrement nextIndex
