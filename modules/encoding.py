import fec
import codecs
fechandler = fec.PacketHandler(key="aausat")

def utf8encode(data:str) -> bytes:
    return fechandler.frame(data.encode("utf-8"))

def utf8decode(data, HMAC_length=2) -> str:
    raw,_,_ = fechandler.deframe(data)
    if raw is not None:
        try:
            return codecs.decode(raw)
        except:
            return codecs.decode(raw[:len(raw)-HMAC_length])
    else:
        print("ERROR: packet seems to be invalid")

if __name__ == "__main__":
    encoded = utf8encode("test")
    print(utf8decode(encoded))
