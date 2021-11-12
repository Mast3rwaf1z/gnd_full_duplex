#gnd imports
import bluebox as bb
import fec

#standard imports
import threading
import time
import binascii

class dualBB_handler():
    def __init__(self, txserial="00000003", rxserial="00000008", rx_freq=145000000, tx_freq=434500000, timeout=10000, modindex=1, bitrate=2400, power=0):
        self.tx = bb.Bluebox(serial=txserial)
        self.rx = bb.Bluebox(serial=rxserial)
        self.tx.tx_mode()
        self.rx.rx_mode()
        self.tx.set_frequency(tx_freq)
        self.rx.set_frequency(rx_freq)
        self.tx.set_power(power)
        self.rx.timeout = 10000
        self.tx.set_bitrate(bitrate)
        self.rx.set_bitrate(bitrate)
        self.fechandler = fec.PacketHandler(key="aausat_secret")


    def transmit(self, packet:str="ping"):
        data = self.fechandler.frame(binascii.hexlify(bytes(packet, "utf-8")))
        self.tx.transmit(data)
        return packet
    
    def receive(self):
        data = None
        while data is None:
            data,rssi,freq = self.rx.receive()
        try:
            packet,_,_ = self.fechandler.deframe(data)
            return packet
        except:
            print(data)
            receive(self)

class tx_thread(threading.Thread):
    def __init__(self, BBH:dualBB_handler):
        threading.Thread.__init__(self)
        self.BBH = BBH
        self.start()
    def run(self):
        while True:
            self.BBH.transmit("test")
            time.sleep(5)

class rx_thread(threading.Thread):
    def __init__(self, BBH:dualBB_handler):
        threading.Thread.__init__(self)
        self.BBH = BBH
        self.start()
    def run(self):
        packetcounter = 0
        while True:
            packetcounter += 1
            packet = self.BBH.receive()
            if packet is not None:
                print(str(packetcounter) + " " + bytes.decode(binascii.unhexlify(packet), "utf-8"))


if __name__ == "__main__":
    BBH = dualBB_handler() #leave blank for default configuration
    txthread = tx_thread(BBH)
    rxthread = rx_thread(BBH)
