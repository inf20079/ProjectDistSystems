from middleware.types.MessageTypes import Coordinate
from control.exceptions import MovementNotPossible

class TrafficArea:
    NO_ID = -1

    def __init__(self, maxPerNode, maxSizeX, maxSizeY):
        self.area = [[[self.NO_ID for _ in range(maxPerNode)] for _ in range(maxSizeY)] for _ in range(maxSizeX)]
        self.clear()

    def remove(self, id, from_coord):
        id_found_and_removed = False
        for i in range(len(self.area[from_coord.x][from_coord.y])):
            if self.area[from_coord.x][from_coord.y][i] == id:
                self.area[from_coord.x][from_coord.y][i] = self.NO_ID
                id_found_and_removed = True
                break
        if not id_found_and_removed:
            raise MovementNotPossible("id not found at start")

    def place(self, id, to_coord):
        free_pos = -1
        for i in range(len(self.area[to_coord.x][to_coord.y])):
            if self.area[to_coord.x][to_coord.y][i] == self.NO_ID:
                free_pos = i
            elif self.area[to_coord.x][to_coord.y][i] == id:
                raise MovementNotPossible("id already placed at target position")
        if free_pos == -1:
            raise MovementNotPossible("no empty space left")
        self.area[to_coord.x][to_coord.y][free_pos] = id

    def getPosition(self, id):
        for x in range(len(self.area)):
            for y in range(len(self.area[x])):
                for client_id_pos in range(len(self.area[x][y])):
                    if self.area[x][y][client_id_pos] == id:
                        return Coordinate(x, y)
        return None

    def isFree(self, position):
        x, y = position.x, position.y
        for client_id_pos in range(len(self.area[x][y])):
            if self.area[x][y][client_id_pos] == self.NO_ID:
                return True
        return False

    def getArea(self):
        return self.area

    def setArea(self, area):
        self.area = area

    def print(self):
        print("############## AREA     ###############")
        for y in range(len(self.area[0])):
            for x in range(len(self.area)):
                to_print = "\t"
                for i in range(len(self.area[x][y])):
                    to_print += " " + str(self.area[x][y][i])
                print("|" + to_print + "|", end="")
            print("")
        print("############## AREA END ###############")

    def clear(self):
        for x in range(len(self.area)):
            for y in range(len(self.area[x])):
                for client_id_pos in range(len(self.area[x][y])):
                    self.area[x][y][client_id_pos] = self.NO_ID
