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