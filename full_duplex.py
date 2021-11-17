import bluebox as bb
import threading

class dualBB_handler():
    def __init__(self, txserial="00000003", rxserial="dead0024", frequency=434500000):
        self.tx = bb.Bluebox(serial=txserial)
        self.rx = bb.Bluebox(serial=rxserial)
        self.tx.tx_mode()
        self.rx.rx_mode()
        self.tx.set_frequency(frequency)
        self.rx.set_frequency(frequency)
        self.tx.set_power(0)

    def transmit(self, packet="ping"):
        self.tx.transmit(bytes(packet, "utf-8"))
    
    def receive(self):
        return self.rx.receive()

def testThread(BB:dualBB_handler):
    while True:
        BB.transmit()

def testThread2(BB:dualBB_handler):
    while True:
        print(BB.receive())

if __name__ == "__main__":
    BB = dualBB_handler()
    threading.Thread.start(testThread)
    threading.Thread.start(testThread2)