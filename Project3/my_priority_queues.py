import math as math

from fontTools.cffLib import privateDictOperators


class ArrayPQ: # use tuples where the priority is the first element and the value is the second element

    def __init__(self, items): # items is a map contianing the item and the prioriryt
        self.queue = []
        self.makeQueue(items)

    def makeQueue(self, items):
        # need to use the distances as keys, distance should always be infinite
        distance = math.inf
        for item in items:
            self.queue.append((distance, item))

    def setPriority(self, node, priority):
        for item in self.queue:
            if item[1] == node:
                newItem = (priority, item[1])
                self.queue.remove(item)
                self.queue.append(newItem)


    def __bool__(self):
        return len(self.queue) == 0

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, item, priority):
        if not item in self.queue:
            self.queue.append((priority, item))

    def deleteMin(self):
        min_val = 0
        for i in range(len(self.queue)):
            if self.queue[i][0] < self.queue[min_val][0]:
                min_val = i
        item = self.queue[min_val][1]
        del self.queue[min_val]
        return item

    def decrease_key(self, node, new_priority):
        for index, (n, priority) in enumerate(self.queue):
            if n == node:
                self.queue[index] = (n, new_priority)
                break




class HeapPQ:
    pass




