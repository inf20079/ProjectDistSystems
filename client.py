import argparse
import configparser
import os
import random
from asyncio import sleep

from client.Client import Client
from middleware.types.MessageTypes import Coordinate


def argparser():
    # Create the parser
    parser = argparse.ArgumentParser(description="Client")

    # Add arguments
    parser.add_argument("-sx", "--size_x", dest="x", type=int, help="The size in x direction of the traffic area.")
    parser.add_argument("-sy", "--size_y", dest="y", type=int, help="The size in y direction of the traffic area.")
    parser.add_argument("-cl", "--clients", dest="amountClients", type=int, help="The amount of clients to create.")
    parser.add_argument("-cfg", "--config", dest="config", type=str, help="Path to cluster config")

    # Parse the arguments
    args, unknown = parser.parse_known_args()

    return args.x, args.y, args.amountClients, args.config


def main():
    x, y, amount, configStr = argparser()

    # config
    config = configparser.ConfigParser()
    config.read(os.getcwd() + os.sep + configStr)

    memberStr = config.get('cluster', 'memberList', fallback='').split(',')
    members = [(config.get(str(id), "ip"), int(config.get(str(id), "port"))) for id in memberStr]

    clients = []
    for clientID in range(amount):
        clients.append(Client(Coordinate(random.randint(1, 1000), random.randint(0, 1000)), members, "localhost", 13000 + clientID, 1000, 1000, clientID))

    for client in clients:
        client.start()

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            for client in clients:
                client.visualize()
            sleep(1)
    except KeyboardInterrupt:
        print("Stopped")
        for client in clients:
            client.shutdown()


if __name__ == "__main__":
    main()
