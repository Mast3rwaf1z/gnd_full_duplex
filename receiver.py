import bluebox as bb

rx:bb.Bluebox

def rx_init(serial="00000002", freq=434500000) -> bb.Bluebox:
    rx = bb.Bluebox(serial=serial)
    rx.rx_mode()
    rx.set_frequency(freq)
    rx.set_modindex(1)
    return rx

def receive(self:bb.Bluebox):
    return self.receive()

if __name__ == "__main__":
    rx = rx_init()
    while True:
        print(receive(rx))
