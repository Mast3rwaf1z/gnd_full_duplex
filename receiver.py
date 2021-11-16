import bluebox as bb

rx:bb.Bluebox

def rx_init(serial="", freq=434500000) -> bb.Bluebox:
    rx = bb.Bluebox(serial)
    rx.rx_mode()
    rx.set_frequency(freq)
    return rx

if __name__ == "__main__":
    rx = rx_init()