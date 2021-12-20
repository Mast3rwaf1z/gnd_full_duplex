#gnd imports
import bluebox as bb

#standard imports
import threading
import time
from modules.data_structures import *

#our project imports
import modules.encoding as encoding

txThread = None
rxThread = None

#create a forward error correction handler object with a shared key

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
        self.rx.set_ifbw(ifbw)
        self.HDBB:bb.Bluebox = None
        self.tq = queue()
        

    #function to transmit data to a satellite
    def transmit(self, tx=None):
        if tx == None:
            tx = self.tx
        if self.tq.size > 0:
            data = encoding.utf8encode(self.tq.pull())
            tx.transmit(data)
    
    #function to receive data from a satellite
    def receive(self, rx=None):
        if rx == None:
            rx = self.rx
        data = None
        while data is None:
            data,_,_ = rx.receive()
        return data

    #if a package containing the signal to switch to half duplex is received, this function is run, it will terminate the transmitting and receiving threads and start one that does those two operations
    def set_half_duplex(self, power=4):
        self.HDBB = self.rx     #the bluebox used is fixed to the one that would require the least reconfiguration
        self.HDBB.set_power(power)
        txThread.stop()
        rxThread.stop()
        print("Successfully enabled half duplex!")
        self.HDBB.transmit(encoding.utf8encode("hdack")) #send an ack to satellite to let it know that it can stop retransmitting signals to start half duplex
        HD_thead = HDThread(self.HDBB, self.tq)
        return True

#if a radio dies on the satellite, this thread will switch on instead of the rx and tx threads to handle the single frequency
class HDThread(threading.Thread):
    def __init__(self, HDBB:bb.Bluebox, tq:queue): #we're renaming the BB object to better suit our needs here
        threading.Thread.__init__(self)
        self.HDBB = HDBB
        self.tq = tq
        time.sleep(4)
        self.start()
    def run(self):
        print("Half duplex thread started")
        while True:
            if self.tq.size > 0:
                self.HDBB.transmit(encoding.utf8encode(self.tq.pull()))
                print("data sent")
            else:
                print("queue empty")
            data = None
            timeouts = 0     #the thought behind using a counter here is to interrupt the attempt to receive in case we missed the packet
            while data is None:
                timeouts += 1
                if timeouts > 3: #it is allowed to timeout 3 times, the timeout is 10000 ms as initialized in the handler
                    break
                data,_,_ = self.HDBB.receive()
            if timeouts > 3: #this essentially does the same as exception handling, it restarts the loop if no packet is received
                continue

            print("received packet")
            print(encoding.utf8decode(data))
            time.sleep(2)



#this thread simply handles continuous calls to the BBH transmit method, the reason this class exists
#is to provide the ability to call the transmit function without a threading class, this will allow
#this program to be configured more in depth than if everything was completely automatic
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

#this class does largely the same as the transmit thread, it just receives in place of transmitting, followed by calling the decoding method

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
            packet = self.BBH.receive() #listen for packets
            if packet is not None:
                decoded = encoding.utf8decode(packet) #decode packet
                if decoded == "sethd": #check if a BB is dead
                    self.BBH.set_half_duplex()

                print(str(packetcounter) + " " + decoded) #print the received packet
        print("full duplex receiving ended") #if loop is broken and thread is ending
    def stop(self): #method to interrupt the thread
        self.receiving = False

if __name__ == "__main__":#some dummy testing to see if it works
    import getpass
    import socket
    BBH = dualBB_handler(txserial="00000008", rxserial="ffffffff", power=4) #leave blank for default configuration
    txThread = tx_thread(BBH, packet="ping from " + getpass.getuser() + '@' + socket.gethostname() + " using " + BBH.tx.serial)
    rxThread = rx_thread(BBH)
    while True:
        BBH.tq.put(input("input some data for the queue: "))
