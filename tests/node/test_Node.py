import unittest
from unittest.mock import MagicMock, patch

from middleware.UnicastInterface import Unicast
from middleware.types.MessageTypes import Message
from node.Node import Node


class TestNode(unittest.TestCase):

    @patch('socket.gethostname', return_value='localhost')
    @patch('socket.gethostbyname', return_value='127.0.0.1')
    def setUp(self, mock_gethostname, mock_gethostbyname):
        self.node = Node(id=1, stateClass=MagicMock())

    def test_send_message_broadcast(self):
        message = "Hello, world!"
        self.node.broadcastInterface.appendMessage = MagicMock()
        self.node.sendMessageBroadcast(message)
        self.node.broadcastInterface.appendMessage.assert_called_once_with(message)

    def test_send_message_unicast(self):
        message = Message(1, 2, 4)
        self.node.unicastInterface.appendMessage = MagicMock()
        self.node.sendMessageUnicast(message)
        self.node.unicastInterface.appendMessage.assert_called_once_with(message)

    def test_get_ip_by_id(self):
        id_to_find = 1
        self.node.peers = {MagicMock(id=1, host='127.0.0.1', port=12001),
                           MagicMock(id=2, host='127.0.0.2', port=12002)}
        self.assertEqual(self.node.getIpByID(id_to_find), [list(self.node.peers)[0]])

    def test_send_discovery(self):
        self.node.broadcastInterface.appendMessage = MagicMock()
        self.node.sendDiscovery()
        self.node.broadcastInterface.appendMessage.assert_called_once()

    def test_on_discovery_response_received(self):
        member1 = MagicMock(id=1, host='127.0.0.1', port=12001)
        member2 = MagicMock(id=2, host='127.0.0.2', port=12002)
        member3 = MagicMock(id=3, host='127.0.0.3', port=12002)
        self.node.peers = {member1}
        message = MagicMock(member=member2, memberList={member3})
        self.node.onDiscoveryResponseReceived(message)
        self.assertEqual(self.node.peers, {member1, member2, member3})

    def tearDown(self) -> None:
        self.node.shutdown()
