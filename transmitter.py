import codecs
import bluebox as bb
import fec


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
    tx.transmit(data)
    return packet

if __name__ == "__main__":
    tx = tx_init()
    transmit(tx)
