import os
import socket
from time import sleep

from middleware.types.MessageTypes import Member
from node.Node import Node
from states.Follower import Follower


def main():

    # Get the hostname of the machine
    hostname = socket.gethostname()
    # Get the IP address associated with the hostname
    ip = socket.gethostbyname(hostname)
    # Get the ID of the node
    id = int(os.environ.get("ID"))
    # Configuration of used ports
    port = 14001
    broadcastPort = 14000
    # Generate peers
    clusterSize = int(os.environ.get('CLUSTERSIZE'))
    peers = [Member(id=i, port=14001, host=str(os.environ.get(f"NODE{i}")))
             for i in range(clusterSize) if i != id]
    # print config
    print(f"[{id}] Config: id={id}, ip={ip}, port={port}, broadcastPort={broadcastPort}, clusterSize={clusterSize}")
    print(f"[{id}] Peers: {peers}")

    # Create node
    node = Node(stateClass=Follower, id=id, ipAddress=str(ip), unicastPort=port,
                broadcastPort=broadcastPort, peers=peers)
    # run logic
    try:
        while True:
            node.pollMessages()
    except KeyboardInterrupt:
        print("Stopped")
        node.shutdown()


if __name__ == "__main__":
    main()
