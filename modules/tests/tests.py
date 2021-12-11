import threading
import time

class bitrate_test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.var = 0
        self.start_time = time.time()
        self.start()
        print("started bitrate test")
    def run(self):
        while True:
            time.sleep(1)
            running_time = time.time() - self.start_time
            with open("bitrate.csv", "a") as file:
                file.write(str(int(running_time)) + ": " + str(self.var) + "\n")
            self.var = 0