import argparse
import configparser
import os
from time import sleep

from middleware.types.MessageTypes import Member
from node.Node import Node
from states.Follower import Follower


def argparser():
    # Create the parser
    parser = argparse.ArgumentParser(description="Node")

    # Add arguments
    parser.add_argument("-id", "--node_id", dest="id", type=int, help="The id of the node")
    parser.add_argument("-cfg", "--config", dest="config", type=str, help="Path to cluster config")

    # Parse the arguments
    args, unknown = parser.parse_known_args()

    return args


def main():
    args = argparser()

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
            sleep(0.0001)
    except KeyboardInterrupt:
        print("Stopped")
        node.shutdown()


if __name__ == "__main__":
    main()
