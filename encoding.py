import fec
import codecs
fechandler = fec.fechandler(key="aausat")

def utf8encode(data:str) -> bytes:
    return fechandler.frame(data.encode("utf-8"))

def utf8decode(data) -> str:
    raw,_,_ = fechandler.deframe()
    return codecs.decode(raw)

if __name__ == "__main__":
    encoded = utf8encode("test")
    print(utf8decode(encoded))
