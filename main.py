from control.TrafficArea import TrafficArea
from middleware.types.MessageTypes import AddEntriesRequest
from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def main():
    # testarea = TrafficArea(2, 3, 4)
    # print(testarea.get_position(2))

    leader = Node(0, Leader(), "")
    follower = Node(1, Follower(), "")

    addEntryMessage = AddEntriesRequest(
        senderID=0,
        receiverID=1,
        term=3,
        commitIndex=4,
        prevLogIndex=4,
        prevLogTerm=2,
        entries=[(5, "command_1"), (6, "command_2"), (7, "command_3")]
    )

    follower.onMessage(addEntryMessage)


if __name__ == '__main__':
    main()

