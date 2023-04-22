import threading
import unittest
import socket
from dataclasses import dataclass
from time import sleep

from middleware.UnicastListener import UnicastListener
from middleware.MulticastPublisher import MulticastPublisher
from middleware.types.MessageTypes import Coordinate


@dataclass
class Listener:
    host: str
    port: int


class TestMulticastPublisher(unittest.TestCase):

    def test_register_listener(self):
        sp = MulticastPublisher()
        sp.registerListener("localhost", 12000)
        self.assertEqual(len(sp.listeners), 1)
        self.assertEqual(sp.listeners[0].host, "localhost")
        self.assertEqual(sp.listeners[0].port, 12000)

    def test_append_message(self):
        sp = MulticastPublisher()
        message = "test message"
        sp.appendMessage(message)
        self.assertEqual(sp.message_queue.qsize(), 1)
        self.assertEqual(sp.message_queue.get(), message)

    #def test_run(self):
    #    sp = UnicastPublisher()
    #    sp.registerListener("localhost", 12000)
    #    message = Coordinate(1, 2)
    #    sp.appendMessage(message)
    #    sl = UnicastListener("localhost", 14000)
    #    sl.start()
    #    sp.start()
#
    #    # check that the message was correctly parsed and added to the queue
    #    parsed_message = sl.popMessage()
    #    self.assertIsNotNone(parsed_message)
    #    self.assertEqual(parsed_message.x, message.x)
    #    self.assertEqual(parsed_message.y, message.y)
#
    #    sp.shutdown()
    #    sp.join()

    def test_shutdown(self):
        sp = MulticastPublisher()
        sp.shutdown()
        self.assertTrue(sp.stop_event.is_set())

    #def append_message(pub, stop_event):
    #    while not stop_event.is_set():
    #        pub.append_message("test message")
    #        sleep(0.5)
