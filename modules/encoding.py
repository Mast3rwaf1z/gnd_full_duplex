#aausat imports
import fec

#standard imports
import codecs

import modules.logs.log as log

#here is the master behind our forward error correction, a library that does the work for us,
#this handler encodes the data with Reed-Solomon encoding
fechandler = fec.PacketHandler(key="aausat")

#here the data is simply using a standard codec in python to encode the data to be sent, followed by framing it with fec
def utf8encode(data:str) -> bytes:
    return fechandler.frame(data.encode("utf-8"))

#here the data received on either end is decoded, some exceptionhandling occours here to ensure the HMAC doesn't interfere with the packet as it is packaged right next to the data
def utf8decode(data, HMAC_length=2) -> str:
    raw,_,_ = fechandler.deframe(data)
    if raw is not None:
        try:
            decoded = codecs.decode(raw)
            log.add("1st_decode.txt") #a little bit of logging to see how we're actually decoding the packets
            return decoded
        except:
            decoded = codecs.decode(raw[:len(raw)-HMAC_length])
            log.add("2nd_decode.txt")
            return decoded
    else:
        print("ERROR: packet seems to be invalid")

#testing
if __name__ == "__main__":
    encoded = utf8encode("test")
    print(utf8decode(encoded))
