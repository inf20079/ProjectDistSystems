import argparse
import json
import socket
from datetime import datetime

from client.Client import Client
from control.TrafficArea import TrafficArea
from middleware.UnicastPublisher import UnicastPublisher, Unicast
from middleware.UnicastListener import UnicastListener
from middleware.types.MessageTypes import Coordinate, NavigationResponse


def argparser():
    # Create the parser
    parser = argparse.ArgumentParser(description="Client")

    # Add arguments
    parser.add_argument("-sx", "--size_x", dest="x", type=int, help="The size in x direction of the traffic area.")
    parser.add_argument("-sy", "--size_y", dest="y", type=int, help="The size in y direction of the traffic area.")
    parser.add_argument("-cl", "--clients", dest="amountClients", type=int, help="The amount of clients to create.")

    # Parse the arguments
    args, unknown = parser.parse_known_args()

    return args.x, args.y, args.amountClients

def main():
    x, y , amount = argparser()
    clients = []
    for clientID in range(amount):
        clients.append(Client())

if __name__ == "__main__":
    main()