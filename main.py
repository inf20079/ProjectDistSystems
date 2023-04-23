import time

from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def main():
    # testarea = TrafficArea(2, 3, 4)
    # print(testarea.get_position(2))

    leader = Node(0, Leader(), None)
    #follower = Node(1, Follower(), None)

    node = Node(0, Follower())

    while True:
        node.pollMessages()
        time.sleep(0.01)


if __name__ == '__main__':
    main()

