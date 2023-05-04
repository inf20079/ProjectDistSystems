from typing import Tuple


class Map:
    def __init__(self, dest_pos: Tuple[int, int], width: int, height: int):
        # Initialize the game board with "-" for every empty space
        self.map = [["-" for _ in range(width)] for _ in range(height)]

        # Set the start and destination positions
        self.dest_pos = dest_pos
        self.current_pos = None

        # Mark the destination positions on the board
        self.map[dest_pos[0]][dest_pos[1]] = "X"

        # print misc
        self.printBorder = " ".join(["#" for _ in range(width+2)])

    def setStart(self, start_pos: Tuple[int, int]):
        self.map[start_pos[0]][start_pos[1]] = "S"
        self.current_pos = start_pos

    def print_board(self):
        # Print the game board to the console
        print(self.printBorder)
        for row in self.map:
            print("# " + " ".join(row) + " #")
        print(self.printBorder)

    def move(self, new_pos):

        if not self.current_pos:
            self.current_pos = new_pos
            return

        # Check if the new position is within the bounds of the board
        if new_pos[0] < 0 or new_pos[0] >= len(self.map) or \
                new_pos[1] < 0 or new_pos[1] >= len(self.map[0]):
            print("Position out of Map")
            return

        # Mark the previous position as "P" and the new position as "C"
        self.map[self.current_pos[0]][self.current_pos[1]] = "P"
        self.map[new_pos[0]][new_pos[1]] = "C"

        # Update the current position
        self.current_pos = new_pos
