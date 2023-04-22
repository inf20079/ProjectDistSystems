import socket
import json
import threading
from time import sleep

from middleware.AbstractSocketListener import AbstractSocketListener


class UnicastListener(AbstractSocketListener):

    def configureSocket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def run(self):
        while True:
            if self.stop_event.is_set():
                break
            client_socket, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.listenToClient, args=(client_socket,))
            client_thread.start()
            self.client_threads.append(client_thread)

        # Clean up client threads
        for thread in self.client_threads:
            thread.join()

    def listenToClient(self, client_socket):
        while True:
            if self.stop_event.is_set():
                break
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            message_parsed = self.parseMessage(message)
            self.message_queue.put(message_parsed)
        client_socket.close()


if __name__ == "__main__":
    sub = UnicastListener("localhost", 12004)
    sub.start()
    while True:
        print(sub.popMessage())
        sleep(0.2)
