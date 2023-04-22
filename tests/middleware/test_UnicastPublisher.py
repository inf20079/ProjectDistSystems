import unittest
from socket import socket
from unittest.mock import patch, MagicMock

from middleware.UnicastPublisher import UnicastPublisher


class TestUnicastPublisher(unittest.TestCase):

    def setUp(self):
        self.host = "localhost"
        self.port = 1234
        self.publisher = UnicastPublisher(self.host, self.port)

    def test_init(self):
        self.assertEqual(self.publisher.host, self.host)
        self.assertEqual(self.publisher.port, self.port)
        self.assertEqual(self.publisher.message_queue.qsize(), 0)
        self.assertFalse(self.publisher.stop_event.is_set())
        self.assertEqual(self.publisher.timeoutevents, 0)

    def test_append_message(self):
        message = {"foo": "bar"}
        self.publisher.appendMessage(message)
        self.assertEqual(self.publisher.message_queue.qsize(), 1)
        self.assertEqual(self.publisher.message_queue.get(), message)

    def test_shutdown(self):
        self.publisher.shutdown()
        self.assertTrue(self.publisher.stop_event.is_set())

