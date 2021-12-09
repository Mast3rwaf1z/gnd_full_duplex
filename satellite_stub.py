import binascii
import codecs
import threading
import time
import os
import bluebox as bb
from data_structures import *

from receiver import rx_init, rx_thread, fechandler
from transmitter import tx_init, tx_thread

txFreq = 431000000
rxFreq = 431200000
packetcounter = 0
tq = queue()

def halfDuplex(bb:bb.Bluebox):
    data = None
    global packetcounter
    packetcounter += 1
    print("attempting to receive a half duplex packet")
    while data is None:
        data,rssi,freq_offset = bb.receive()
    file = open("packets/data" + packetcounter)
    file.write(utf8decode(data))
    file.close()
    file = open("packets/data" + packetcounter, "r")
    print("received: " + file.read())
    print("transmitting a half duplex packet")
    bb.transmit(utf8encode("received half duplex packet!"))

def utf8decode(data:bytes) -> str:
    HMAC_LENGTH=2
    try:
        
        packet,_,_ = fechandler.decode(data)
    
        if packet is not None:
            try:
                return binascii.unhexlify(bytes.decode(codecs.decode(packet)))
            except:
                return binascii.unhexlify(bytes.decode(codecs.decode(packet[:len(packet)-HMAC_LENGTH])))
    except:
        print("ERROR: fec broke")
        return 0

def utf8encode(data:str):
    return fechandler.frame(codecs.encode(bytes(data, "utf-8")))

def bbcheck(tx:bb.Bluebox, rx:bb.Bluebox) -> int:
    try:
        tx.get_frequency()
        try:
            rx.get_frequency()
            #tx on rx on
            return 0
        except:
            #tx on rx off
            return 1
    except:
        try:
            rx.get_frequency()
            #tx off rx on
            return 2
        except:
            #tx off rx off
            return 3


if __name__ == "__main__":
    txThread = None
    rxThread = None
    tx:bb.Bluebox = None
    ack = False
    while tx == None:
        try:
            #break
            tx = tx_init(serial="dead0024", power=16, freq=txFreq, bitrate=4800)
        except Exception as e:
            print("no transmitter plugged in")
            print(e)
            time.sleep(5)
            continue
    rx:bb.Bluebox = None
    while rx == None:
        try:
            #break
            rx = rx_init(serial="00000003", power=0, freq=rxFreq, bitrate=4800)
        except Exception as e:
            print("no receiver plugged in")
            print(e)
            time.sleep(5)
            continue
    input("ready? (y/n) ")


    while True:
        state = bbcheck(tx, rx)
        if state == 0:
            rx.get_frequency()
            #start full duplex
            if txThread == None:
                txThread = tx_thread(tx, tq)
                print("started txthread")
            if rxThread == None:
                rxThread = rx_thread(rx)
                print("started rxthread")
            elif rxThread.tstop:
                print("stopping transmission")
                txThread.stop_transmit()
                rxThread.tstop = False
            arg = input("send some data or file: ")
            if arg == "file":
                file = open("Shrek.txt")
                data = file.read()
                i = 0
                while i<len(data):
                    packet = data[i:i+40]
                    i += 40
                    txThread.tq.put(packet)

            time.sleep(10)
        if state == 1:
            if not txThread == None:
                txThread.stop()
                txThread = None
            if not ack:
                packet = None
                while packet is None:
                    tx.transmit(utf8encode("sethd"))
                    packet,_,_ = tx.receive()
                if utf8decode(packet) == "hdack":
                    ack = True
            #start half duplex
            halfDuplex(tx)
        if state == 2:
            if not rxThread == None:
                rxThread.stop()
                rxThread = None
            rx.set_frequency(txFreq)
            if not ack:
                packet = None
                while packet is None:
                    rx.transmit(utf8encode("sethd"))
                    packet,_,_ = rx.receive()
                if utf8decode(packet) == "hdack":
                    ack = True
            #start half duplex
            halfDuplex(rx)
        if state == 3:
            print("no blueboxes found")

