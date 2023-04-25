import time

from middleware.types.MessageTypes import Member
from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def main():
    nodes = []
    nodeCount = 3

    members = [Member(id=i, host="localhost", port=12004 + i * 2) for i in range(nodeCount)]

    for i in range(nodeCount):
        peers = members.copy()
        del peers[i]
        nodes.append(Node(i, Follower(),
                          ipAddress="localhost",
                          unicastPort=members[i].port,
                          broadcastPort=12005,
                          peers=peers)
                     )

    while True:
        for node in nodes:
            node.pollMessages()
        # time.sleep(0.01)


if __name__ == '__main__':
    main()
