import math as math # old, stable, works, don't touch.

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
        self.setPriority(node, new_priority)







class HeapPQ:

    # so I think the way that we are going to do this is by implemtning tuples again, where the first number is the priority and the second is the value.

    def __init__(self, items):
        self.heap = []
        self.index_map = {}
        self.makeHeap(items)

    def isEmpty(self):
        return len(self.heap) == 0

    def makeHeap(self, items):
        distance = math.inf
        for item in items:
            self.heap.append((distance, item))
            self.index_map[item] = len(self.heap) - 1

    def parent(self, i):
        return (i -1) // 2 # basically because we can assume that its filled all the way we can do some weird stuff mathmatically

    def left_child(self, i):
        return (2 * i) + 1

    def right_child(self, i):
        return (2 * i) + 2

    def insert(self, item, priority):
        self.heap.append((priority, item))
        self.heapify_up(len(self.heap)-1)
        self.index_map[item] = len(self.heap)-1

    def heapify_up(self, i):
        while i > 0 and self.heap[i][0] < self.heap[self.parent(i)][0]: # make sure we are sorting by priority here
            self.swap(i, self.parent(i))
            self.index_map[self.heap[i][1]] = i # adjusts the input map appropriately.
            self.index_map[self.heap[self.parent(i)][1]] = self.parent(i)
            i = self.parent(i)

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.index_map[self.heap[i][1]] = i
        self.index_map[self.heap[j][1]] = j

    def heapify_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            left = self.left_child(i)
            right = self.right_child(i)

            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest != i:
                self.swap(i, smallest)
                self.index_map[self.heap[i][1]] = i
                self.index_map[self.heap[smallest][1]] = smallest
                i = smallest

            else:
                break


    def deleteMin(self): # so the problem is that I need this to be a min heap, not a max heap. maybe.
        if len(self.heap) == 0:
            return None

        item = self.heap[0][1]
        last_item = self.heap.pop()
        self.heap[0] = self.heap[-1]
        self.index_map[last_item[1]] = 0
        self.heapify_down(0)
        del self.index_map[item]
        return item


    def setPriority(self, node, priority):
        index = self.index_map[node]
        current_priority = self.heap[index][0]
        self.heap[index] = (priority, node)
        if priority < current_priority:
            self.heapify_up(index)
        else:
            self.heapify_down(index)



    def decrease_key(self, node, new_priority):
        self.setPriority(node, new_priority)

