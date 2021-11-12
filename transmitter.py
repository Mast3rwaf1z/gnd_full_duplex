import codecs
import bluebox as bb
import fec
<<<<<<< HEAD
import binascii

def tx_init(serial="00000003", freq=434500000, power=8, mod=1, bitrate=9200) -> bb.Bluebox:
    tx = bb.Bluebox(serial=serial) #get serial key from bbctl list
    tx.tx_mode()
    tx.set_frequency(freq)
    tx.set_power(power)
    tx.set_modindex(mod)
    tx.set_bitrate(bitrate)
    return tx

def transmit(tx:bb.Bluebox, packet:str = "ping") -> tuple:
    fecc = fec.PacketHandler(key="test")
    data = fecc.frame(binascii.hexlify(bytes(packet, "utf-8")))
=======


def tx_init(serial="00000003", freq=434500000) -> bb.Bluebox:
    tx = bb.Bluebox(serial=serial) #get serial key from bbctl list
    tx.tx_mode()
    tx.set_frequency(freq)
    tx.set_power(4)
    tx.set_modindex(1)
    return tx

def transmit(tx:bb.Bluebox, packet:str = "ping") -> tuple:
    fecc = fec.PacketHandler(key="nickersej")
    data = fecc.frame(codecs.encode("0x00f2448e01"))
>>>>>>> c4a4ed47811072ac550f8860fdcf6aaf0833a4d4
    tx.transmit(data)
    return packet

if __name__ == "__main__":
<<<<<<< HEAD
    tx = tx_init(bitrate=2400, power=0)
    transmit(tx, input("input:"))
=======
    tx = tx_init()
    transmit(tx)
>>>>>>> c4a4ed47811072ac550f8860fdcf6aaf0833a4d4
