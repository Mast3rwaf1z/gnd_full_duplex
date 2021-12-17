import time
import bluebox as bb
from modules.data_structures import *
import modules.encoding as encoding

from modules.receiver import rx_init, rx_thread
from modules.transmitter import tx_init, tx_thread

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
    decoded = encoding.utf8decode(data)
    if decoded is not None:
        file = open("packets/data" + str(packetcounter), "w")
        file.write(decoded)
        file.close()
        file = open("packets/data" + str(packetcounter), "r")
        print("received: " + file.read())
        file.close()
        print("transmitting a half duplex packet")
        bb.transmit(encoding.utf8encode("acknowledgement"))

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
            tx = tx_init(serial="02010001", power=0, freq=txFreq, bitrate=4800)
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
        match bbcheck(tx, rx):
            case 0:
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
                    file = open("modules/tests/Shrek.txt")
                    data = file.read()
                    i = 0
                    while i<len(data):
                        packet = data[i:i+40]
                        i += 40
                        txThread.tq.enqueue(packet)

                time.sleep(10)
            case 1:
                if not txThread == None:
                    txThread.stop()
                    txThread = None
                if not rxThread == None:
                    rxThread.stop()
                    rxThread = None
                if not ack:
                    packet = None
                    while packet is None:
                        print("attempting to set half duplex")
                        tx.transmit(encoding.utf8encode("sethd"))
                        packet,_,_ = tx.receive()
                        if encoding.utf8decode(packet) == "hdack":
                            ack = True
                #start half duplex
                halfDuplex(tx)
            case 2:
                if not txThread == None:
                    txThread.stop()
                    rxThread = None
                if not rxThread == None:
                    rxThread.stop()
                    rxThread = None
                rx.set_frequency(txFreq)
                if not ack:
                    packet = None
                    while packet is None:
                        print("attempting to set half duplex")
                        rx.transmit(encoding.utf8encode("sethd"))
                        packet,_,_ = rx.receive()
                        if encoding.utf8decode(packet) == "hdack":
                            ack = True
                #start half duplex
                halfDuplex(rx)
            case 3:
                print("no blueboxes found")

