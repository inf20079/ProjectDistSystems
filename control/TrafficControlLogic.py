from control.TrafficArea import TrafficArea
from middleware.types.MessageTypes import Coordinate
from control.exceptions import MovementNotPossible
from math import sqrt, pow


class TrafficControlLogic:
    def __init__(self, trafficArea):
        self.trafficArea: TrafficArea = trafficArea

    def start(self, id):
        currentPosition = self.trafficArea.getPosition(id)
        if currentPosition is None:
            for y in range(len(self.trafficArea.getArea()[0])):
                pos = Coordinate(0, y)
                if self.trafficArea.isFree(pos):
                    self.trafficArea.place(id, pos)
                    return pos

            raise MovementNotPossible("no free position found")
        else:
            raise MovementNotPossible("client already available")

    def move(self, id, targetToReach):
        currentPosition = self.trafficArea.getPosition(id)
        bestCoordinate = currentPosition
        distance = self.getDistance(bestCoordinate, targetToReach)

        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                x = currentPosition.x + xOffset
                y = currentPosition.y + yOffset

                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                if x > len(self.trafficArea.getArea()) - 1:
                    x = len(self.trafficArea.getArea()) - 1
                if y > len(self.trafficArea.getArea()[0]) - 1:
                    y = len(self.trafficArea.getArea()[0]) - 1

                coordinateToCheck = Coordinate(x, y)
                if self.trafficArea.isFree(coordinateToCheck):
                    newDistance = self.getDistance(coordinateToCheck, targetToReach)
                    if newDistance < distance:
                        distance = newDistance
                        bestCoordinate = coordinateToCheck

        self.trafficArea.remove(id, currentPosition)
        self.trafficArea.place(id, bestCoordinate)
        return bestCoordinate

    def getDistance(self, firstCoordinate, secondCoordinate):
        x1 = firstCoordinate.x
        x2 = secondCoordinate.x
        y1 = firstCoordinate.y
        y2 = secondCoordinate.y

        if x1 == x2 and y1 == y2:
            return 0.0
        else:
            return sqrt(
                pow(x1 - x2, 2) + pow(y1 - y2, 2)
            )
