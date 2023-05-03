import json
import threading
from datetime import datetime
import random
from typing import Tuple, List

from client.Map import Map
from middleware.UnicastInterface import UnicastInterface, Unicast
from middleware.types.MessageTypes import Coordinate, NavigationResponse, NavigationRequest


class Client(threading.Thread):

    def __init__(self, destination: Coordinate, serverList: List[Tuple[str, int]], ip: str, port: int, sizeX: int, sizeY: int, clientID: int):
        super().__init__()
        self.serverList = serverList
        self.id = clientID
        self.ip = ip
        self.port = port
        self.destination = destination
        self.destinationReached = False
        self.currentPosition = None
        self.stopEvent = threading.Event()
        # Map
        self.map = Map((destination.x, destination.y), sizeX, sizeY)
        # communication
        self.unicastInterface = UnicastInterface(self.ip, self.port)
        # time tracking
        self.startTime = None
        self.endTime = None

    def run(self) -> None:
        while not self.destinationReached and not self.stopEvent.is_set():
            self.unicastInterface.refresh()
            message = self.unicastInterface.popMessage()
            if isinstance(message, NavigationResponse):
                self.onNavigation(message)
        print(f"Reached destination in: {self.getTimeDiff()}")

    def onNavigation(self, message: NavigationResponse):
        self.currentPosition = message.nextStep
        if self.currentPosition == self.destination:
            self.destinationReached = True
        else:
            self.map.move((message.nextStep.x, message.nextStep.y))
            self.requestNavigation()
        print(f"At time {self.getTimeDiff()} at position {self.currentPosition}.")

    def requestNavigation(self):
        serverAdress = random.choice(self.serverList)
        message = NavigationRequest(self.id, self.currentPosition, self.destination)
        unicast = Unicast(serverAdress[0], serverAdress[{1}], message)
        self.unicastInterface.appendMessage(unicast)

    def setStartTime(self):
        self.startTime = datetime.now()

    def setEndTime(self):
        self.endTime = datetime.now()

    def getTimeDiff(self):
        if self.endTime:
            return self.endTime - self.startTime
        else:
            return datetime.now() - self.startTime

    def shutdown(self):
        self.stopEvent.set()
