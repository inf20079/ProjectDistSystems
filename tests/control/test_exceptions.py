from unittest import TestCase

from control.exceptions import MovementNotPossible


class TestMovementNotPossible(TestCase):

    def test_creation(self):
        error_message = "test error message"
        movement_not_possible = MovementNotPossible(error_message)
        self.assertEqual(str(movement_not_possible), error_message)