import bluebox as bb
import fec
import codecs
import binascii
import threading


rx:bb.Bluebox
fechandler = fec.PacketHandler(key="aausat")

def rx_init(serial="dead0024", freq=439000000, mod=1, timeout=10000, bitrate=2400, ifbw=1, power=8) -> bb.Bluebox:
    rx = bb.Bluebox(serial=serial)
    rx.rx_mode()
    rx.set_frequency(freq)
    rx.set_modindex(mod)
    rx.timeout = timeout
    rx.set_bitrate(bitrate)
    rx.set_ifbw(ifbw)
    rx.set_power(power)
    return rx

def receive(self:bb.Bluebox):
    data = None
    while data is None:
        data,rssi,freq = self.receive()
    packet,_,_ = fechandler.deframe(data)
    return packet

class rx_thread(threading.Thread):
    def __init__(self, rx:bb.Bluebox):
        threading.Thread.__init__(self)
        self.receiving = True
        self.rx = rx
        self.tstop = False
        self.start()
    def run(self):
        packetcounter = 0
        while self.receiving:
            packet = None
            try:
                packet = receive(self.rx)
            except Exception as e:
                print(e)
            #print("received full duplex packet")
            if packet is not None:
                packetcounter += 1
                data = open("packets/data" + str(packetcounter), "w")
                data.write(bytes.decode(binascii.unhexlify(codecs.decode(packet))))
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
            print(str(packetcounter) + " " + bytes.decode(binascii.unhexlify(packet), "utf-8"))
