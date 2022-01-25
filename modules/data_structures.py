class queue():
    #some definitions native to python, will enable functionality as to get a representative when calling
    #obj instead of obj.size and functionality to len
    def __init__(self):
        self.items = []
        self.size = 0
    def __len__(self):
        return self.size
    def __repr__(self):
        return str(self.items)
    #data structure design by the book
    def enqueue(self, item):
        self.items.append(item)
        self.size += 1
    def dequeue(self):
        if self.size > 0:
            self.size -= 1
            return self.items.pop(0)
        else: 
            return None
    def clear(self):
        self.__init__()



if __name__ == "__main__":
    Q = queue()
    for i in range(10):
        Q.enqueue(i)
    print(str(len(Q))+str(Q))
    Q.dequeue()
    print(str(len(Q))+str(Q))
