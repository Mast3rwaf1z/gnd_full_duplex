import bluebox as bb

tx = bb.Bluebox("") #get serial key from bbctl list
tx.tx_mode()
tx.set_frequency(434500000)

tx.transmit(bytes(input("input: "), "utf-8"))

