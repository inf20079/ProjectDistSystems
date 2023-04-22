import socket
import json
import unittest
from unittest.mock import MagicMock

from middleware.BroadcastPublisher import BroadcastPublisher
from middleware.types.JsonCoding import EnhancedJSONEncoder


class TestBroadcastPublisher(unittest.TestCase):
    def setUp(self):
        self.port = 12345
        self.broadcaster = BroadcastPublisher(self.port)

    def test_broadcast(self):
        data = {"message": "Hello, world!"}

        # Create a mock socket object and replace the original socket with it
        self.broadcaster.sock = MagicMock(spec=socket.socket)

        self.broadcaster.broadcast(data)

        # Check that the message was sent to the correct port
        expected_address = ("<broadcast>", self.port)
        sent_message, sent_address = self.broadcaster.sock.sendto.call_args[0]
        self.assertEqual(sent_address, expected_address)

        # Check that the message was encoded and sent as expected
        expected_message = json.dumps(data, cls=EnhancedJSONEncoder).encode()
        self.assertEqual(sent_message, expected_message)

    def tearDown(self):
        self.broadcaster.sock.close()


if __name__ == '__main__':
    unittest.main()
