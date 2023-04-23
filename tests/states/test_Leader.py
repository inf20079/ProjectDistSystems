import unittest

from node.Node import Node, LogEntry
from states.Leader import Leader
from middleware.types.MessageTypes import AppendEntriesResponse


class TestLeader(unittest.TestCase):
    def setUp(self):
        self.leader = Leader()
        self.leaderNode = Node(0, self.leader, None, [1, 2],
                               [LogEntry(0, "a"), LogEntry(0, "b"), LogEntry(1, "c")])

    def test_onResponseReceived_Successful(self):
        message = AppendEntriesResponse(
            senderID=1,
            receiverID=0,
            term=1,
            success=True
        )

        self.assertEqual(self.leader.onResponseReceived(message), (self.leader, None))
        self.assertEqual(self.leader.nextIndex[1], 2)
        # ToDo: matchIndex

    def test_onResponseReceived_Failed(self):
        message = AppendEntriesResponse(
            senderID=1,
            receiverID=0,
            term=0,
            success=False
        )

        state, response = self.leader.onResponseReceived(message)

        self.assertEqual(state, self.leader)
        self.assertIsNotNone(response)
        self.assertEqual(self.leader.nextIndex[1], 2)  # decrement nextIndex
