# Implementation plan
The plan for this chapter is to have an introduction about what we first made, then some background knowledge about the things we used in the initial design, then the final features added to the software.

-   A figure, class diagram
## full duplex design
-   Two bluebox micros connected only to USB
-   A raspberry pi 4 running armv7 Arch Linux ARM and has bbctl installed
## What is bbctl
-   Software designed to interface with bluebox transceivers
-   Features?
    -   command line encoding
        -   fec integrated
    -   python interface
## Half duplex compatibility design
-   A handler for when a satellite radio "dies"
    -   we'll call this bbcheck, it is part of the satellite_stub program
-   switch to the correct frequency
## Data structures
-   file
    -   managing packet storage in a seperate directory
-   our queue
```python
class queue():
    def __init__(self):
        self.items = []
        self.size = 0
    def put(self, item):
        self.items.append(item)
        self.size += 1
    def pull(self):
        if self.size > 0:
            self.size -= 1
            return self.items.pop(0)
        else: 
            return None
```
## encoding
-   insert the encoding types used
    -   fec
    -   bytes
        -   utf-8
        -   codecs
    -   old stuff
        -   binascii
-   the implementation
    ```python
    def utf8encode(data:str) -> bytes:
    return fechandler.frame(data.encode("utf-8"))

    def utf8decode(data, HMAC_length=2) -> str:
        try: 
            raw,_,_ = fechandler.deframe(data)
        except Exception as e:
            print(e)
            return
        if raw is not None:
            try:
                decoded = codecs.decode(raw)
                log.add("1st_decode.txt") 
                return decoded
            except:
                decoded = codecs.decode(raw[:len(raw)-HMAC_length])
                log.add("2nd_decode.txt")
                return decoded
    ```
## Test prep
-   GUI
    -   queue button
    -   text field to send plain text packets
    -   initialisation button
-   continuous satellite transmission
    -   a stop function
