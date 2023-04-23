import time
import unittest
from unittest.mock import MagicMock
from middleware.types.MessageTypes import RequestVoteMessage
from node.Node import Node
from states.Voter import Voter


class TestVoter(unittest.TestCase):

    def setUp(self):
        self.voter = Voter()
        self.voter.node = MagicMock()
        self.voter.node.lastLogIndex.return_value = 9
        self.voter.node.currentTerm = 1

    def test_onVoteRequestReceived_votedFor_is_None(self):
        message = RequestVoteMessage(senderID=1, receiverID=0, term=1, lastLogIndex=9, lastLogTerm=1)
        state, response = self.voter.onMessage(message)

        self.assertEqual(state, self.voter)
        self.assertTrue(response.voteGranted)
        self.assertEqual(self.voter.votedFor, 1)

    def test_onVoteRequestReceived_votedFor_is_not_None(self):
        message = RequestVoteMessage(senderID=1, receiverID=0, term=1, lastLogIndex=9, lastLogTerm=1)
        self.voter.votedFor = 2
        state, response = self.voter.onMessage(message)

        self.assertEqual(state, self.voter)
        self.assertFalse(response.voteGranted)
        self.assertEqual(self.voter.votedFor, 2)

    def test_onVoteRequestReceived_less_up_to_date_log(self):
        message = RequestVoteMessage(senderID=1, receiverID=0, term=1, lastLogIndex=8, lastLogTerm=1)
        state, response = self.voter.onMessage(message)

        self.assertEqual(state, self.voter)
        self.assertFalse(response.voteGranted)
        self.assertIsNone(self.voter.votedFor)

    def test_resetElectionTimeout(self):
        self.voter.nextElectionTimeout = 100
        self.voter.resetElectionTimeout()
        self.assertAlmostEquals(self.voter.nextElectionTimeout, time.time() + self.voter.electionTimeout)
