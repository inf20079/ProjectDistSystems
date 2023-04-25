import threading
import time


class RecurringProcedure:

    def __init__(self, timeout, onTimeouted):
        self.active = True
        self.timeout = timeout
        self.onTimeouted = onTimeouted

        self.nextTimeout = 0

    def start(self):
        self.resetTimeout()
        threading.Thread(
            target=self.watchHeartbeatTimeout
        ).start()

    def watchHeartbeatTimeout(self):
        while self.active:
            while time.time() >= self.nextTimeout and self.active:  # wait for reset
                time.sleep(0.01)
            while time.time() < self.nextTimeout and self.active:  # count down
                time.sleep(0.01)
            if self.active:
                self.onTimeouted()

    def resetTimeout(self):
        self.nextTimeout = time.time() + self.timeout

    def shutdown(self):
        # print(f"(Recurring Procedure) shutdown")
        self.active = False
