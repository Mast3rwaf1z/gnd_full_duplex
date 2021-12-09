import codecs
import socket
import getpass
import threading
import bluebox as bb
import fec
import binascii
import time
from data_structures import *
fecc = fec.PacketHandler(key="aausat")

def tx_init(serial="dead0024", freq=145000000, power=0, mod=1, bitrate=2400, ifbw=1, timeout=10000) -> bb.Bluebox:
    tx = bb.Bluebox(serial=serial) #get serial key from bbctl list
    tx.tx_mode()
    tx.set_frequency(freq)
    tx.set_power(power)
    tx.set_modindex(mod)
    tx.set_bitrate(bitrate)
    tx.set_ifbw(ifbw)
    tx.timeout = timeout
    return tx

def transmit(tx:bb.Bluebox, packet:str = "ping") -> tuple:
    data = fecc.frame(binascii.hexlify(bytes(packet, "utf-8")))
    tx.transmit(data)
    return packet

class tx_thread(threading.Thread):
    def __init__(self, tx:bb.Bluebox, tq:queue):
        threading.Thread.__init__(self)
        self.transmitting = True
        self.tx = tx
        self.tq = tq
        self.start()
    def run(self):
        while self.transmitting:
            if self.tq.size>0:
                try:
                    transmit(self.tx, self.tq.pull())
                except:
                    print("transmitter might have been disconnected, exiting")
                    return
            else:
                try:
                    transmit(self.tx, "beacon from " + getpass.getuser() + '@' + socket.gethostname() +" using "+ self.tx.serial)
                except:
                    print("transmitter might have been disconnected, exiting")
                    return
            time.sleep(5)
    def stop(self):
        self.transmitting = False
    def stop_transmit(self):
        while self.tq.size>0:
            self.tq.pull()

if __name__ == "__main__":
    tx = tx_init(power=13, freq=431000000)
    while True:
        transmit(tx, "ping from " + getpass.getuser() + '@' + socket.gethostname() +" using "+ tx.serial)
        time.sleep(5)
