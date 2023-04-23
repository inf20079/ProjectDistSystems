import unittest

from middleware.types.MessageTypes import RequestVoteMessage
from node.Node import Node
from states.Candidate import Candidate
from states.Follower import Follower


class TestFollower(unittest.TestCase):
    def test_onVoteRequestReceived(self):
        # Create a node and a candidate
        followerNode = Node(1, Follower())

        # Create a vote request from a different node
        vote_request = RequestVoteMessage(
            senderID=2,
            receiverID=1,
            term=1,
            lastLogIndex=0,
            lastLogTerm=0
        )

        # Call the on_vote_request_received method with the vote request
        followerNode.onMessage(vote_request)

        # Verify that the candidate's current term is now 1
        self.assertEqual(followerNode.currentTerm, 1)

        # Verify that the candidate has granted its vote to the other node
        self.assertEqual(followerNode.state.votedFor, 2)

        # Verify that the candidate's election timeout has been reset
        self.assertEqual(followerNode.state.currElectionTimeout, 0)
