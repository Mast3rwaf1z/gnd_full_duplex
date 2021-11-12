import bluebox as bb

rx:bb.Bluebox

def rx_init(serial="dead0024", freq=434500000) -> bb.Bluebox:
    rx = bb.Bluebox(serial=serial)
    rx.rx_mode()
    rx.set_frequency(freq)
    return rx

def receive(self:bb.Bluebox) -> str:
    return self.receive()

if __name__ == "__main__":
    rx = rx_init()
    while True:
        print(receive(rx))
