#gnd imports
import bluebox as bb
import fec

#standard imports
import threading
import time
import binascii
import codecs
from data_structures import *

txThread = None
rxThread = None

#create a forward error correction handler object with a shared key
fechandler = fec.PacketHandler(key="aausat")

#it is time to create a queue data structure such that when the system is gonna transmit, it will only do so if the queue is not empty
#for the system not to break completely, we will require that the method returns a string and only a string, and adds a string and only a string to the queue

#this class is made such that the gnd would only have to interface with a handler that acts as a single hardware, even though it is handling multiple
#the variables defined here are default values and test values, these can be changed at object creation to suit the specific setup
class dualBB_handler():
    def __init__(self, txserial="00000003", rxserial="ffffffff", rx_freq=431000000, tx_freq=431200000, timeout=10000, modindex=1, bitrate=2400, ifbw=1, power=0):
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
        self.HDBB:bb.Bluebox = None
        self.tq = queue()
        

    #function to transmit data to a satellite
    def transmit(self, tx=None):
        if tx == None:
            tx = self.tx
        if self.tq.size > 0:
            data = fechandler.frame(binascii.hexlify(bytes(self.tq.pull(), "utf-8")))
            tx.transmit(data)
        time.sleep(1)
    
    #function to receive data from a satellite
    def receive(self, rx=None):
        if rx == None:
            rx = self.rx
        data = None
        while data is None:
            data,_,_ = rx.receive()
        try:#a little bit of exception handling
            packet,_,_ = fechandler.deframe(data) #remove forward error correction before ending the receive function
            return packet
        except:
            print("ERROR: failed to get a valid packet")
            self.receive() #recursion to continue receiving

    #if a package containing the signal to switch to half duplex is received, this function is run, it will terminate the transmitting and receiving threads and start one that does those two operations
    def set_half_duplex(self, power=0):
        self.HDBB = self.rx     #the bluebox used is fixed to the one that would require the least reconfiguration
        self.HDBB.set_power(power)
        txThread.stop()
        rxThread.stop()
        print("Successfully enabled half duplex!")
        self.HDBB.transmit(fechandler.frame(binascii.hexlify(bytes("hdack", "utf-8")))) #send an ack to satellite to let it know that it can stop retransmitting signals to start half duplex
        HD_thead = HDThread(self.HDBB, self.tq)
        return True

class HDThread(threading.Thread):
    def __init__(self, HDBB, tq:queue):
        threading.Thread.__init__(self)
        self.HDBB = HDBB
        self.tq = tq
        time.sleep(4)
        self.start()
    def run(self):
        HMAC_LEN = 2
        print("Half duplex thread started")
        while True:
            if self.tq.size > 0:
                self.HDBB.transmit(fechandler.frame(binascii.hexlify(bytes(self.tq.pull(), "utf-8"))))
                print("data sent")
            else:
                print("queue empty")
            data = None
            counter = 0
            while data is None:
                counter += 1
                if counter > 3:
                    break
                data,_,_ = self.HDBB.receive()
            if counter > 3:
                continue
            try:
                packet,_,_ = fechandler.decode(data)
            except Exception as e:
                print(e)

            print("received packet")
            if packet is not None:
                print(packet)
                print(bytes.decode(binascii.unhexlify(packet[:len(packet)-HMAC_LEN]), "utf-8"))
            time.sleep(2)




class tx_thread(threading.Thread):
    def __init__(self, BBH:dualBB_handler):
        threading.Thread.__init__(self)
        self.BBH = BBH
        self.transmitting = True
        self.start()
        print("transmit thread started")
    def run(self):
        while self.transmitting:
            self.BBH.transmit()
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
                if decoded == "sethd":
                    self.BBH.set_half_duplex()

                print(str(packetcounter) + " " + decoded)
        print("full duplex receiving ended")
    def stop(self):
        self.receiving = False

if __name__ == "__main__":
    import getpass
    import socket
    BBH = dualBB_handler(txserial="00000008", rxserial="ffffffff", power=4) #leave blank for default configuration
    txThread = tx_thread(BBH, packet="ping from " + getpass.getuser() + '@' + socket.gethostname() + " using " + BBH.tx.serial)
    rxThread = rx_thread(BBH)
    while True:
        BBH.tq.put(input("input some data for the queue: "))
