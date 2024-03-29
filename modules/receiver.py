#standard
import threading
import time

#aausat
import bluebox as bb

#our project
import modules.tests.tests as tests
import modules.encoding as encoding

rx:bb.Bluebox

def rx_init(serial="dead0024", freq=439000000, mod=1, timeout=10000, bitrate=2400, ifbw=2, power=8) -> bb.Bluebox:
    rx = bb.Bluebox(serial=serial)
    rx.rx_mode()
    rx.set_frequency(freq)
    rx.set_modindex(mod)
    rx.timeout = timeout
    rx.set_bitrate(bitrate)
    rx.set_ifbw(ifbw)
    rx.set_power(power)
    return rx

def receive(self:bb.Bluebox, bitrateTest:tests.bitrate_test):
    data = None
    while data is None:
        data,rssi,freq = self.receive()
    if bitrateTest is not None:
        bitrateTest.var += len(data)
    return data

class rx_thread(threading.Thread):
    def __init__(self, rx:bb.Bluebox):
        threading.Thread.__init__(self)
        self.receiving = True
        self.rx = rx
        self.tstop = False
        self.bitrateTest = tests.bitrate_test()
        self.start()
    def run(self):
        packetcounter = 0
        while self.receiving:
            packet = None
            try:
                packet = receive(self.rx, self.bitrateTest)
            except Exception as e:
                print(e)
                continue
            if packet is not None:
                packetcounter += 1
                data = open("packets/data" + str(packetcounter), "w")
                packet = encoding.utf8decode(packet)
                if packet is not None:
                    data.write(packet)
                    data.close()
                    data = open("packets/data" + str(packetcounter), "r")
                    recv = data.read()
                    print(recv, end="")
                    if recv == "tstop":
                        self.tstop = True
    def stop(self):
        self.receiving = False

if __name__ == "__main__":
    rx = rx_init(serial="00000008", freq=431000000)
    packetcounter = 0
    while True:
        packet = receive(rx)
        if packet is not None:
            packetcounter += 1
            print(packet)
            print(str(packetcounter) + " " + encoding.utf8decode(packet))
