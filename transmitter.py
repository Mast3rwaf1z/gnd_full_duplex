import codecs
import bluebox as bb
import fec
import binascii
import time

def tx_init(serial="dead0024", freq=145000000, power=8, mod=1, bitrate=2400) -> bb.Bluebox:
    tx = bb.Bluebox(serial=serial) #get serial key from bbctl list
    tx.tx_mode()
    tx.set_frequency(freq)
    tx.set_power(power)
    tx.set_modindex(mod)
    tx.set_bitrate(bitrate)
    return tx

def transmit(tx:bb.Bluebox, packet:str = "ping") -> tuple:
    fecc = fec.PacketHandler(key="aausat_secret")
    data = fecc.frame(binascii.hexlify(bytes(packet, "utf-8")))
    tx.transmit(data)
    return packet

if __name__ == "__main__":
    tx = tx_init(power=13)
    while True:
        transmit(tx, "test2")
        time.sleep(5)
