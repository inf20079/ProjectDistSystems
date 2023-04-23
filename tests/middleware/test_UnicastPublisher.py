from socket import socket
import unittest
import socket
from time import sleep
from unittest.mock import patch

from middleware.UnicastPublisher import UnicastPublisher, Unicast


class TestUnicastPublisher(unittest.TestCase):
    def test_sendUnicast(self):
        message = {"data": "Hello World"}
        unicast = Unicast("localhost", 8888, message)
        expected_message = b'{"data": "Hello World"}'

        with patch("socket.socket") as mock_socket:
            mock_s = mock_socket.return_value.__enter__.return_value
            mock_s.sendall.return_value = None

            publisher = UnicastPublisher()
            publisher.sendUnicast(unicast)

            mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
            mock_s.connect.assert_called_once_with(("localhost", 8888))
            mock_s.sendall.assert_called_once_with(expected_message)



    def test_appendMessage(self):
        publisher = UnicastPublisher()
        message1 = Unicast("localhost", 8888, {"data": "Hello World"})
        message2 = Unicast("localhost", 8888, {"data": "Goodbye World"})

        publisher.appendMessage(message1)
        publisher.appendMessage(message2)

        self.assertEqual(publisher.message_queue.qsize(), 2)
        self.assertEqual(publisher.message_queue.get(), message1)
        self.assertEqual(publisher.message_queue.get(), message2)

    def test_run(self):
        publisher = UnicastPublisher()
        message = Unicast("localhost", 8888, {"data": "Hello World"})
        publisher.appendMessage(message)

        with patch("threading.Thread.join") as mock_join:
            publisher.start()
            publisher.shutdown()
            publisher.join()

            mock_join.assert_called_once()

    def test_sendThreadsCleanedUp(self):
        publisher = UnicastPublisher()
        message1 = Unicast("localhost", 8888, {"data": "Hello World"})
        message2 = Unicast("localhost", 8888, {"data": "Goodbye World"})

        with patch("middleware.UnicastPublisher.UnicastPublisher.sendUnicast") as mock_send:
            publisher.appendMessage(message1)
            publisher.appendMessage(message2)
            publisher.start()
            sleep(1)
            publisher.shutdown()
            publisher.join()

            mock_send.assert_called()
            self.assertEqual(2, len(publisher.send_threads))


