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
        
        self.fechandler = fec.PacketHandler(key="aausat_secret")


    def transmit(self, packet:str="ping", tx=None):
        if tx == None:
            tx = self.tx
        data = self.fechandler.frame(binascii.hexlify(bytes(packet, "utf-8")))
        tx.transmit(data)
        return packet
    
    def receive(self, rx=None):
        if rx == None:
            rx = self.rx
        data = None
        while data is None:
            data,rssi,freq = rx.receive()
        try:
            packet,_,_ = self.fechandler.deframe(data)
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
        return True
    
    def halfDuplexToggle(self):
        #to be mccd toggleable tranceiving mode
        pass


    def halfDuplex(self):
        self.transmit("half duplex first ping", tx=self.HDBB)
        self.receive(rx=self.HDBB)


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
    def stop():
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
                print(str(packetcounter) + " " + bytes.decode(binascii.unhexlify(packet), "utf-8"))
        print("full duplex receiving ended")
    def stop():
        self.receiving = False


if __name__ == "__main__":
    BBH = dualBB_handler(power=8) #leave blank for default configuration
    txthread = tx_thread(BBH, packet="ping from " + getpass.getuser() + '@' + socket.gethostname() + " using " + BBH.tx.serial)
    rxthread = rx_thread(BBH)
