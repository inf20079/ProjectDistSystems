import unittest
from unittest.mock import Mock, patch
from middleware.types.MessageTypes import ResponseVoteMessage, RequestVoteMessage
from node.Node import Node
from states.Candidate import Candidate
from states.Follower import Follower
from states.Leader import Leader


class TestCandidate(unittest.TestCase):

    def setUp(self):
        self.candidateNode = Node(0, Candidate())
        self.candidateNode.peers = [1, 2, 3, 4]

    def test_onVoteResponseReceived_higherTerm(self):
        # Test case where response message has a higher term than the candidate's current term

        message = ResponseVoteMessage(senderID=1, receiverID=0, term=2, voteGranted=False)
        state, response = self.candidateNode.onMessage(message)

        self.assertTrue(isinstance(state, Follower))
        self.assertIsNone(response)

    def test_onVoteResponseReceived_voteGranted(self):
        # Test case where the vote is granted

        message = ResponseVoteMessage(senderID=1, receiverID=0, term=self.candidateNode.currentTerm, voteGranted=True)
        state, response = self.candidateNode.onMessage(message)

        self.assertEqual(self.candidateNode.state.votesReceived, 2)
        self.assertEqual(state, self.candidateNode.state)
        self.assertIsNone(response)

    def test_onVoteResponseReceived_voteNotGranted(self):
        # Test case where the vote is not granted

        message = ResponseVoteMessage(senderID=1, receiverID=0, term=self.candidateNode.currentTerm, voteGranted=False)
        state, response = self.candidateNode.onMessage(message)

        self.assertEqual(self.candidateNode.state.votesReceived, 1)
        self.assertEqual(state, self.candidateNode.state)
        self.assertIsNone(response)

    def test_onVoteResponseReceived_majorityVotes(self):
        # Test case where candidate receives votes from a majority of the cluster
        message1 = ResponseVoteMessage(senderID=1, receiverID=0, term=self.candidateNode.currentTerm, voteGranted=True)
        message2 = ResponseVoteMessage(senderID=2, receiverID=0, term=self.candidateNode.currentTerm, voteGranted=False)
        message3 = ResponseVoteMessage(senderID=3, receiverID=0, term=self.candidateNode.currentTerm, voteGranted=True)
        self.candidateNode.onMessage(message1)
        self.candidateNode.onMessage(message2)
        state, response = self.candidateNode.onMessage(message3)

        self.assertEqual(state, self.candidateNode.state)
        self.assertTrue(isinstance(state, Leader))
        self.assertIsNone(response)

    def test_startElection(self):
        # Test case for starting an election

        self.candidateNode.state.startElection()

        self.assertEqual(self.candidateNode.currentTerm, 2) # ToDo: Not sure why 2 and not 1
        self.assertEqual(self.candidateNode.state.votedFor, self.candidateNode.id)
        self.assertEqual(self.candidateNode.state.votesReceived, 1)
        # self.assertEqual(response.senderID, self.candidateNode.id)
        # self.assertEqual(response.receiverID, -1)
        # self.assertEqual(response.term, self.candidateNode.currentTerm)
        # self.assertEqual(response.lastLogIndex, len(self.candidateNode.log) - 1)
        # self.assertEqual(response.lastLogTerm, self.candidateNode.log[-1].term if len(self.candidateNode.log) > 0 else -1)
