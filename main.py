import time

from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def main():
    node = Node(0, Follower())

    while True:
        node.pollMessages()
        time.sleep(0.01)


if __name__ == '__main__':
    main()

