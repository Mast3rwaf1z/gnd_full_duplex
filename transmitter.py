import bluebox as bb

tx:bb.Bluebox

def tx_init(serial="", freq=434500000) -> bb.Bluebox:
    tx = bb.Bluebox(serial) #get serial key from bbctl list
    tx.tx_mode()
    tx.set_frequency(freq)
    return tx

if __name__ == "__main__":
    tx = tx_init()
    while True:
        tx.transmit(bytes(input("input: "), "utf-8"))