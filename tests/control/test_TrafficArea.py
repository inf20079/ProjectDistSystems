from unittest import TestCase

from control.TrafficArea import TrafficArea
from control.exceptions import MovementNotPossible
from middleware.types.MessageTypes import Coordinate


class TestTrafficArea(TestCase):

    def setUp(self):
        self.traffic_area: TrafficArea = TrafficArea(3, 4, 4)

    def test_remove(self):
        self.traffic_area.place(1, Coordinate(0, 0))
        self.traffic_area.place(2, Coordinate(1, 1))
        self.traffic_area.place(3, Coordinate(2, 2))
        self.traffic_area.remove(1, Coordinate(0, 0))
        self.assertIsNone(self.traffic_area.getPosition(1))
        with self.assertRaises(MovementNotPossible):
            self.traffic_area.remove(1, Coordinate(0, 0))

    def test_place(self):
        self.traffic_area.place(1, Coordinate(0, 0))
        self.assertEqual(self.traffic_area.getPosition(1), Coordinate(0, 0))
        with self.assertRaises(MovementNotPossible):
            self.traffic_area.place(1, Coordinate(0, 0))
        self.traffic_area.place(3, Coordinate(3, 3))
        self.traffic_area.place(4, Coordinate(3, 3))
        self.traffic_area.place(5, Coordinate(3, 3))
        with self.assertRaises(MovementNotPossible):
            self.traffic_area.place(2, Coordinate(3, 3))

    def test_getPosition(self):
        self.traffic_area.place(1, Coordinate(0, 0))
        self.assertEqual(self.traffic_area.getPosition(1), Coordinate(0, 0))
        self.assertIsNone(self.traffic_area.getPosition(2))

    def test_isFree(self):
        self.assertTrue(self.traffic_area.isFree(Coordinate(0, 0)))
        self.traffic_area.place(1, Coordinate(0, 0))
        self.traffic_area.place(2, Coordinate(0, 0))
        self.traffic_area.place(3, Coordinate(0, 0))
        self.assertFalse(self.traffic_area.isFree(Coordinate(0, 0)))

    def test_clear(self):
        self.traffic_area.place(1, Coordinate(0, 0))
        self.traffic_area.clear()
        self.assertIsNone(self.traffic_area.getPosition(1))
