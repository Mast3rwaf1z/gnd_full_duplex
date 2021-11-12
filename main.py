import threading
import time
import bluebox as bb




class transmitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tx = bb.Bluebox(serial="00000003")
        self.tx.tx_mode()
        self.tx.set_frequency(freq=434500000)
    def run(self):
        self.tx.set_power(4)
        while(True):
            time.sleep(1)
            print("transmitting")
            self.tx.transmit(bytes("test", "utf-8"))

class receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rx = bb.Bluebox(serial="dead0024")
        self.rx.rx_mode()
        self.rx.set_frequency(freq=434500000)
    def run(self):
        while(True):
            time.sleep(1)
            print("receiving")
            print(self.rx.receive()[0])

rx = receiver()
tx = transmitter()
rx.start()
tx.start()