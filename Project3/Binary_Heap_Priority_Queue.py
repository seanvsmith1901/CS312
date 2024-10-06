class Priority_Queue_With_Heap:
    # filled with all the stub functions that I will need to implement in order to make sure all is well.

    # so the dictionary implementation is much easier which is why he told us to do that first
    # for this implementation, we will need an array to represent the approximate ordering, a dictionary to map items to the priorities
    # and a dictionary to map items to positions in the heap array. Wooh.

    # whenever an item moves through the heap, you need to update the item:position dictionary!

    # assume no negative cycles.


    def __init__(self):
        self.heap = [None]

    def parent(self, i):
        return (i -1) // 2 # basically because we can assume that its filled all the way we can do some weird stuff mathmatically

    def left_child(self, i):
        return (2 * i) + 2

    def right_child(self, i):
        return (2 * i) + 2

    def insert(self, item):
        self.heap.append(item)
        self.heapify_up(len(self.heap)-1)

    def heapify_up(self, i):
        while i > 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i] # the fetching AI wrote all that for me. fetch that.

    def heapify_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            left = self.left_child(i)
            right = self.right_child(i)

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != i:
                self.swap(i, smallest)
                i = smallest

            else:
                break


    def deleteMin(self): # so the problem is that I need this to be a min heap, not a max heap. maybe.
        pass

    def decreaseKey(self, item, key):

        pass






