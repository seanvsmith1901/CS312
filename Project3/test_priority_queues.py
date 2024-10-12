from my_priority_queues import ArrayPQ, HeapPQ


def test_pqs():
    items = list(range(10))
    array_pq = ArrayPQ(items)
    heap_pq = HeapPQ(items)

    array_pq.setPriority(7, 7)
    heap_pq.setPriority(7, 7)

    assert array_pq.deleteMin() == 7
    assert heap_pq.deleteMin() == 7

    array_pq.setPriority(3, 3)
    array_pq.setPriority(5, 1)
    heap_pq.setPriority(3, 3)
    heap_pq.setPriority(5, 1)

    assert array_pq.deleteMin() == 5
    assert array_pq.deleteMin() == 3

    assert heap_pq.deleteMin() == 5
    assert heap_pq.deleteMin() == 3
