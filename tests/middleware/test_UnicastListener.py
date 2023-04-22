import unittest
import socket
import time
import json

from middleware.UnicastListener import UnicastListener


class TestUnicastListener(unittest.TestCase):

    def test_listen_and_parse(self):
        # create a new SocketListener instance
        listener = UnicastListener('localhost', 8000)

        # start the listener thread
        listener.start()

        # create a new client socket and connect to the listener
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8000))

        # send a JSON message to the listener
        message = {'x': 1, 'y': 2}
        client_socket.sendall(json.dumps(message).encode())

        # wait for the message to be parsed and added to the message queue
        time.sleep(1)

        # check that the message was correctly parsed and added to the queue
        parsed_message = listener.popMessage()
        self.assertIsNotNone(parsed_message)
        self.assertEqual(parsed_message.x, message['x'])
        self.assertEqual(parsed_message.y, message['y'])

        # shut down the listener thread
        listener.shutdown()
        listener.join()