import heapq
import math
from priority_queues import *



def find_shortest_path_with_heap(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:

    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    distance = {}
    previous = {}
    for node in graph:
        distance[node] = math.inf
        previous[node] = None

    distance[source] = 0

    H = HeapPQ(graph) # should use the distances as keys, we shall see. I don't think this is workign the way that I want it to.

    while H: # that should do the trick lol
        current_node = H.__next__() # that should give us our current_min and delete it from the heap
        for weight in graph[current_node]:
            if distance[graph[current_node][weight]] > distance[current_node] + weight:
                distance[graph[current_node][weight]] = distance[current_node] + weight
                previous[graph[current_node][weight]] = current_node
                H.set_priority(graph[current_node][weight], weight) # ??




        # for edge, weight in graph[current_node]:  # graph[current_node][weight] = edge
        #     if distance[edge] > distance[current_node] + weight:
        #         distance[current_node] = distance[edge] + weight
        #         previous[edge] = current_node
        #         H.set_priority(edge, distance[edge]) # no clue if that works, we shall see.


    # makes the list that we get to return
    return_previous = []
    previous_node = target
    while previous_node != source:
        return_previous.append(previous[previous_node])
        previous_node = previous[previous_node]



    return return_previous, distance[target] # something like that









def find_shortest_path_with_array(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """

    distance = {}
    previous = {}
    for node in graph:
        distance[node] = math.inf
        previous[node] = None

    distance[source] = 0

    pq = ArrayPQ(graph) # should use the distances as keys, we shall see.

    while pq: # that should do the trick lol
        current_node = pq.next()
        for edge in graph[current_node]:
            if distance[edge] > distance[edge] + distance[target]:
                distance[edge] = distance[edge] + distance[target]
                previous[edge] = current_node
                pq.set_priority(edge, distance[edge]) # something like that?


    return(previous[target], distance[target])





