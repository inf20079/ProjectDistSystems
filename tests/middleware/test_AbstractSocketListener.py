import json
import threading
import unittest
from unittest.mock import Mock, patch
from queue import Queue

from middleware.AbstractSocketListener import AbstractSocketListener


class TestAbstractSocketListener(unittest.TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.port = 1234

    def tearDown(self):
        pass

    @patch("middleware.AbstractSocketListener.AbstractSocketListener.__abstractmethods__", set())
    def test_popMessage_empty_queue(self):
        listener = AbstractSocketListener(self.host, self.port)
        self.assertIsNone(listener.popMessage())

    @patch("middleware.AbstractSocketListener.AbstractSocketListener.__abstractmethods__", set())

    def test_popMessage_nonempty_queue(self):
        listener = AbstractSocketListener(self.host, self.port)
        message = Mock()
        listener.message_queue.put(message)
        self.assertEqual(listener.popMessage(), message)

    @patch("middleware.AbstractSocketListener.AbstractSocketListener.__abstractmethods__", set())
    def test_parseMessage_coordinate(self):
        coord_dict = {'x': 1, 'y': 2}
        message = AbstractSocketListener.parseMessage(coord_dict)
        self.assertEqual(message.x, coord_dict['x'])
        self.assertEqual(message.y, coord_dict['y'])

    # repeat for other message types
