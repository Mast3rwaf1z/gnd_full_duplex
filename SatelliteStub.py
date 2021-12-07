import binascii
from logging import exception
import time
import bluebox as bb

from receiver import rx_init, rx_thread, fechandler
from transmitter import tx_init, tx_thread

txFreq = 431000000
rxFreq = 431200000

def halfDuplex(bb:bb.Bluebox):
    data = None
    print("attempting to receive a half duplex packet")
    while data is None:
        data,rssi,freq_offset = bb.receive()
    print("received: " + utf8decode(data))
    print("transmitting a half duplex packet")
    bb.transmit(utf8encode("received half duplex packet!"))

def utf8decode(data:bytes) -> str:
    HMAC_LENGTH=2
    try:
        packet,_,_ = fechandler.decode(data)
    
        if packet is not None:
            try:
                return bytes.decode(binascii.unhexlify(packet), "utf-8")
            except:
                return bytes.decode(binascii.unhexlify(packet[:len(packet)-HMAC_LENGTH]))
    except:
        print("ERROR: fec broke")
        return 0

def utf8encode(data:str):
    return fechandler.frame(binascii.hexlify(bytes(data, "utf-8")))

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
            tx = tx_init(serial="00000003", power=0, freq=txFreq) #working BB
        except:
            print("no transmitter plugged in")
            time.sleep(5)
            continue
    rx:bb.Bluebox = None
    while rx == None:
        try:
            #break
            rx = rx_init(serial="dead0024", power=4, freq=rxFreq) #broken BB
        except:
            print("no receiver plugged in")
            time.sleep(5)
            continue
    input("ready? (y/n) ")


    while True:
        state = bbcheck(tx, rx)
        if state == 0:
            rx.get_frequency()
            #start full duplex
            if txThread == None:
                txThread = tx_thread(tx)
                print("started txthread")
            if rxThread == None:
                rxThread = rx_thread(rx)
                print("started rxthread")
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

