import bluebox as bb

tx:bb.Bluebox

def tx_init(serial="00000003", freq=434500000) -> bb.Bluebox:
    tx = bb.Bluebox(serial=serial) #get serial key from bbctl list
    tx.tx_mode()
    tx.set_frequency(freq)
    return tx

def tx_transmit(tx:bb.Bluebox, packet:str = "ping") -> tuple:
    tx.transmit(bytes(packet, "utf-8"))
    return packet

if __name__ == "__main__":
    tx = tx_init()
    while True:
        tx_transmit(tx, input("input: "))