import unittest
from unittest.mock import patch, MagicMock

from middleware.UnicastInterface import UnicastInterface, Unicast


class TestUnicastInterface(unittest.TestCase):

    def setUp(self):
        # Set up mock socket
        self.mock_socket = MagicMock()
        self.mock_socket.getpeername.return_value = ('mock_host', 1234)
        self.mock_socket.accept.return_value = (self.mock_socket, ('mock_client', 5678))
        self.mock_socket.recv.return_value = b'{}'
        self.mock_socket.sendall.return_value = None
        self.mock_socket.setblocking.return_value = None

        # Set up UnicastInterface instance
        self.interface = UnicastInterface('localhost', 1234)
        self.interface.socket.close()
        self.interface.socket = self.mock_socket

    def test_appendMessage(self):
        # Test message is added to send queue
        message = Unicast('mock_host', 5678, {'key': 'value'})
        self.interface.appendMessage(message)
        self.assertEqual(self.interface.sendQueue['mock_host5678'], [{'key': 'value'}])

    def test_onWritable(self):
        # Test message is sent on writable socket
        message = Unicast('mock_host', 5678, {'key': 'value'})
        self.interface.sendQueue['mock_host5678'] = [message.message]
        self.interface.clientSockets = [self.mock_socket]
        self.interface.onWritable(self.mock_socket)
        self.mock_socket.sendall.assert_called_once_with(b'{}')

    def test_onReadable(self):
        # Test message is received on readable socket
        self.interface.onReadable()
        self.mock_socket.recv.assert_called_once_with(1024)

    def test_listenToClient(self):
        # Test message is received from client and added to receive queue
        self.mock_socket.recv.return_value = b'{"key": "value"}'
        self.interface.listenToClient(self.mock_socket)
        self.assertEqual(self.interface.receiveQueue, [{'key': 'value'}])

    def test_refresh(self):
        # Test that refresh calls onWritable and onReadable
        with patch.object(self.interface, 'onWritable') as mock_onWritable:
            with patch.object(self.interface, 'onReadable') as mock_onReadable:
                self.interface.refresh()
                mock_onWritable.assert_called_once_with(self.mock_socket)
                mock_onReadable.assert_called_once()

    def tearDown(self):
        self.interface.__del__()
