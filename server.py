import configparser
import os

from middleware.types.MessageTypes import Member
from node.Node import Node
from states.Follower import Follower


def main():

    # config
    config = configparser.ConfigParser()
    config.read(os.getcwd() + os.sep + args.config)

    ip = config.get(str(args.id), "ip")
    port = config.get(str(args.id), "port")
    broadcastPort = config.get("cluster", "broadcastPort")

    # Convert the ports string to a list of integers
    memberStr = config.get('cluster', 'memberList', fallback='').split(',')
    members = [Member(id=int(id), port=int(config.get(str(id), "port")), host=config.get(str(id), "ip")) for id in
               memberStr]
    peers = [member for member in members if member.id != args.id]

    node = Node(stateClass=Follower, id=args.id, ipAddress=str(ip), unicastPort=int(port),
                broadcastPort=int(broadcastPort), peers=peers)

    try:
        while True:
            node.pollMessages()
    except KeyboardInterrupt:
        print("Stopped")
        node.shutdown()


if __name__ == "__main__":
    main()
