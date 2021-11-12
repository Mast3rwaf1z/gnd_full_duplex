#gnd imports
import bluebox as bb
import fec

#standard imports
import threading
import time
import binascii
import codecs
import getpass
import socket

txThread = None
rxThread = None

fechandler = fec.PacketHandler(key="aausat_secret")

class dualBB_handler():
    def __init__(self, txserial="00000003", rxserial="00000008", rx_freq=431000000, tx_freq=439000000, timeout=10000, modindex=1, bitrate=2400, ifbw=1, power=0):
        self.tx = bb.Bluebox(serial=txserial)
        self.rx = bb.Bluebox(serial=rxserial)
        self.tx.tx_mode()
        self.rx.rx_mode()
        self.tx.set_frequency(tx_freq)
        self.rx.set_frequency(rx_freq)
        self.tx.set_power(power)
        self.rx.timeout = timeout
        self.tx.set_bitrate(bitrate)
        self.rx.set_bitrate(bitrate)
        self.tx.set_modindex(modindex)
        self.rx.set_modindex(modindex)
        self.tx.set_ifbw(ifbw)
        self.HDBB = None
        


    def transmit(self, packet:str="ping", tx=None):
        if tx == None:
            tx = self.tx
        data = fechandler.frame(binascii.hexlify(bytes(packet, "utf-8")))
        tx.transmit(data)
        return packet
    
    def receive(self, rx=None):
        if rx == None:
            rx = self.rx
        data = None
        while data is None:
            data,rssi,freq = rx.receive()
        try:
            packet,_,_ = fechandler.deframe(data)
            return packet
        except:
            print("ERROR: failed to get a valid packet")
            self.receive()

    def setHalfDuplex(self, recvFreq, txThread, rxThread):
        if recvFreq == self.rx.get_frequency():
            self.HDBB = self.rx
        elif recvFreq == self.tx.get_frequency():
            self.HDBB = self.tx
        else:
            print("ERROR: set half duplex method failed!")
            return False
        self.HDBB.power = self.tx.get_power()
        self.HDBB.timeout = self.rx.timeout
        txThread.stop()
        rxThread.stop()
        print("Successfully enabled half duplex!")
        HD_thead = HDThread(self.HDBB)
        return True

class HDThread(threading.Thread):
    def __init__(self, HDBB):
        threading.Thread.__init__(self)
        self.HDBB = HDBB
        time.sleep(4)
        self.start()
    def run(self):
        print("Half duplex thread started")
        while True:
            self.HDBB.tx_mode()
            print("data sent")
            self.HDBB.transmit(fechandler.frame(binascii.hexlify(bytes("ping", "utf-8"))))
            self.HDBB.receive()
            time.sleep(2)




class tx_thread(threading.Thread):
    def __init__(self, BBH:dualBB_handler, packet="test"):
        threading.Thread.__init__(self)
        self.BBH = BBH
        self.transmitting = True
        self.packet = packet
        self.start()
        print("transmit thread started")
    def run(self):
        while self.transmitting:
            self.BBH.transmit(self.packet)
            time.sleep(5)
        print("full duplex transmission ended")
    def stop(self):
        self.transmitting = False

class rx_thread(threading.Thread):
    def __init__(self, BBH:dualBB_handler):
        threading.Thread.__init__(self)
        self.BBH = BBH
        self.receiving = True
        self.start()
        print("receive thread started")
    def run(self):
        packetcounter = 0
        while self.receiving:
            packetcounter += 1
            packet = self.BBH.receive()
            if packet is not None:
                decoded = bytes.decode(binascii.unhexlify(packet), "utf-8")
                if decoded == "rxoff":
                    self.BBH.setHalfDuplex(self.BBH.rx.get_frequency(), self, txThread)
                elif decoded == "txoff":
                    self.BBH.setHalfDuplex(self.BBH.tx.get_frequency(), self, txThread)
                print(str(packetcounter) + " " + decoded)
        print("full duplex receiving ended")
    def stop(self):
        self.receiving = False

if __name__ == "__main__":
    BBH = dualBB_handler(power=0) #leave blank for default configuration
    txThread = tx_thread(BBH, packet="ping from " + getpass.getuser() + '@' + socket.gethostname() + " using " + BBH.tx.serial)
    rxThread = rx_thread(BBH)
