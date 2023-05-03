from contextlib import redirect_stdout
import unittest
import io

from client.Map import Map


class MapTest(unittest.TestCase):

    def test_init(self):
        # Test if the game board is initialized with the correct size and "-" characters
        m = Map((0, 0), 2, 3)
        print(m.map)
        self.assertEqual([["X", "-"], ["-", "-"], ["-", "-"]], m.map)
        self.assertEqual(m.dest_pos, (0, 0))

    def test_set_start(self):
        # Test if the start position is set correctly
        m = Map((1, 1), 3, 3)
        m.setStart((0, 0))
        self.assertEqual([["S", "-", "-"], ["-", "X", "-"], ["-", "-", "-"]], m.map)
        self.assertEqual(m.current_pos, (0, 0))

    def test_print_board(self):
        # Test if the board is printed correctly
        m = Map((1, 2), 4, 2)
        expected_output = "# # # # # #\n# - - - - #\n# - - X - #\n# # # # # #\n"
        with io.StringIO() as buf, redirect_stdout(buf):
            m.print_board()
            self.assertEqual(expected_output, buf.getvalue())

    def test_move(self):
        # Test if the move method updates the board and current position correctly
        m = Map((2, 2), 4, 4)
        self.assertEqual(m.map, [["-", "-", "-", "-" ],
                                  ["-", "-", "-", "-"],
                                  ["-", "-", "X", "-"],
                                  ["-", "-", "-", "-"]])

        # Test if move method returns error when current_pos is not set
        with io.StringIO() as buf, redirect_stdout(buf):
            m.move((0, 0))
            self.assertEqual(buf.getvalue(), "Start pos id self.current_pos=None. Please set start pos.\n")

        m.setStart((1, 1))
        m.move((1, 2))
        self.assertEqual(m.current_pos, (1, 2))
        self.assertEqual(m.map, [["-", "-", "-", "-" ],
                                  ["-", "P", "C", "-"],
                                  ["-", "-", "X", "-"],
                                  ["-", "-", "-", "-"]])

        # Test if move method returns error when new position is out of the map
        with io.StringIO() as buf, redirect_stdout(buf):
            m.move((4, 4))
            self.assertEqual(buf.getvalue(), "Position out of Map\n")

