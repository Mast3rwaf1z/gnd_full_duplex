import bluebox as bb
import fec
import codecs
import binascii


rx:bb.Bluebox
fechandler = fec.PacketHandler(key="test")


def rx_init(serial="dead0024", freq=434500000, mod=1, timeout=10000, bitrate=9200) -> bb.Bluebox:
    rx = bb.Bluebox(serial=serial)
    rx.rx_mode()
    rx.set_frequency(freq)
    rx.set_modindex(mod)
    rx.timeout = timeout
    rx.set_bitrate(bitrate)
    return rx

def receive(self:bb.Bluebox):
    data = None
    while data is None:
        data,rssi,freq = self.receive()
    #codecs.decode(data[0],"0x00f2448e01")
    packet,_,_ = fechandler.deframe(data)
    return packet


if __name__ == "__main__":
    rx = rx_init(bitrate=2400)
    while True:
        packet = receive(rx)
        if packet is not None:
            print(bytes.decode(binascii.unhexlify(packet), "utf-8"))
