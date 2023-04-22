from control.TrafficArea import TrafficArea
from middleware.types.MessageTypes import AddEntryMessage
from node.Node import Node
from states.Follower import Follower
from states.Leader import Leader


def main():
    # testarea = TrafficArea(2, 3, 4)
    # print(testarea.get_position(2))

    leader = Node(0, Leader(), "")
    follower = Node(1, Follower(), "")

    addEntryMessage = AddEntryMessage(
        senderID=0,
        receiverID=1,
        term=0,
        commit=True,
        success=True,
        newLogEntry="{}",
        lastLogIndex=-1
    )

    follower.onMessage(addEntryMessage)


if __name__ == '__main__':
    main()

