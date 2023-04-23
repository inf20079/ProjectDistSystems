from control.TrafficArea import TrafficArea
from middleware.types.MessageTypes import AppendEntriesRequest
from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def createCluster(nodeCount = 3):
    for i in range(nodeCount):
        Node(i, Follower())

def main():
    # testarea = TrafficArea(2, 3, 4)
    # print(testarea.get_position(2))

    createCluster(3)


if __name__ == '__main__':
    main()

