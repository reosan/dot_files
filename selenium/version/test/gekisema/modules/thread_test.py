import threading
import time

class fetch():
    def __init__(self):
        self.thread = threading.Thread(self.run, daemon=True)

    def start(self):
        self.thread.start()

    def run(self):
        self.timer = threading.Timer(1.0, self.run)
        self.timer.start()
        print('fetch')
