import time

from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def main():
    nodes = []
    nodeCount = 3
    for i in range(nodeCount):
        nodes.append(Node(i, Follower(),
                          unicastPort=12004 + i * 2,
                          broadcastPort=12005 + i * 2)
                     )

    while True:
        for node in nodes:
            node.pollMessages()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
