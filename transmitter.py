import codecs
import bluebox as bb
import fec
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
    tx.transmit(data)
    return packet

if __name__ == "__main__":
    tx = tx_init(bitrate=2400, power=8)
    transmit(tx, input("input:"))
