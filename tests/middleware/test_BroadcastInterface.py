import select
import socket
import unittest
from unittest.mock import MagicMock

from middleware.BroadcastInterface import BroadcastInterface
from middleware.types.MessageTypes import RequestVoteMessage, Member


class TestBroadcastInterface(unittest.TestCase):

    def setUp(self):
        self.mock_socket = MagicMock(spec=socket.socket)
        self.mock_socket.recvfrom.return_value = (b'{"id": 1, "host":"host", "port": 2}', ("127.0.0.1", 1234))
        self.interface = BroadcastInterface(1234)
        self.interface.socket.close()
        self.interface.socket = self.mock_socket

    def tearDown(self):
        del self.interface

    def test_on_readable(self):
        self.interface.onReadable()
        self.assertEqual(self.interface.receiveQueue, [Member(1, "host", 2)])

    def test_on_writable(self):
        self.interface.sendQueue.append({"lastLogIndex": 1, "lastLogTerm": 2})
        self.interface.onWritable()
        self.mock_socket.sendto.assert_called_once_with(b'{"lastLogIndex": 1, "lastLogTerm": 2}', ("<broadcast>", 1234))

    def test_del(self):
        self.interface.__del__()
        self.mock_socket.close.assert_called_once()
