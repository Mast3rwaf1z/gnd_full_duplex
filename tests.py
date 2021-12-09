import threading
import time

class bitrate_test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.var = 0
        self.start()
        print("started bitrate test")
    def run(self):
        while True:
            time.sleep(1)
            print(self.var)
            self.var = 0
