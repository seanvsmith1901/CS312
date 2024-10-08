class ArrayPQ:

    # So I think for this one I will need to use a dictionary, where the key is the object and the attribute is the priority, so lets change that here first.

    def __init__(self):
        self.queue = []

    def makeQueue(self, item, priority):
        for item in items:
            self.queue.append(item)

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, item, priority):
        self.queue[item] = priority

    def deleteMin(self):
        min_val = 0
        for key in self.queue:
            if self.queue[key] > self.queue[max_val]:
                max_val = self.queue[key]
        item = self.queue[max_val]
        del self.queue[max_val]
        return item



class HeapPQ:
    pass




