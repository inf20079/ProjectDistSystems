from unittest import TestCase

from control.TrafficArea import TrafficArea
from control.exceptions import MovementNotPossible
from middleware.types.MessageTypes import Coordinate
from control.TrafficControlLogic import TrafficControlLogic


class TestTrafficControlLogic(TestCase):

    def setUp(self):
        # Set up a TrafficArea object for testing
        self.area = TrafficArea(1, 10, 10)
        self.traffic_control = TrafficControlLogic(self.area)

    def test_start(self):
        # Test starting a client at a free position
        pos = self.traffic_control.start(1)
        self.assertEqual(pos, Coordinate(0, 0))
        self.assertFalse(self.area.isFree(pos))

        # Test starting a client that already exists
        with self.assertRaises(MovementNotPossible):
            self.traffic_control.start(1)

        # Test starting a client when no free positions exist
        for i in range(2, 11):
            self.traffic_control.start(i)

        with self.assertRaises(MovementNotPossible):
            self.traffic_control.start(10)

    def test_move(self):
        # Test moving a client to a nearby position
        self.traffic_control.start(1)
        pos = self.traffic_control.move(1, Coordinate(1, 0))
        self.assertEqual(pos, Coordinate(1, 0))
        self.assertFalse(self.area.isFree(pos))
