import unittest

from node.Node import Node
from states.Leader import Leader
from middleware.types.MessageTypes import AppendEntriesResponse, LogEntry


class TestLeader(unittest.TestCase):
    def setUp(self):
        self.leaderNode = Node(0, Leader, peers=[1, 2],
                               log=[LogEntry(0, "a"), LogEntry(0, "b"), LogEntry(1, "c")])
        self.leader = self.leaderNode.state

    def tearDown(self):
        self.leaderNode.shutdown()

    def test_onResponseReceived_Successful(self):
        message = AppendEntriesResponse(
            senderID=1,
            receiverID=0,
            term=1,
            success=True
        )

        stateClass, response = self.leader.onResponseReceived(message)

        self.assertEqual(stateClass, Leader)
        self.assertIsNone(response)
        self.assertEqual(self.leader.nextIndex[1], 2)
        # ToDo: matchIndex

    def test_onResponseReceived_Failed(self):
        message = AppendEntriesResponse(
            senderID=1,
            receiverID=0,
            term=0,
            success=False
        )

        stateClass, response = self.leader.onResponseReceived(message)

        self.assertEqual(stateClass, Leader)
        self.assertIsNotNone(response)
        self.assertEqual(self.leader.nextIndex[1], 2)  # decrement nextIndex
