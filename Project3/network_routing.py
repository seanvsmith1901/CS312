import math
from my_priority_queues import ArrayPQ, HeapPQ # add the hashmap to this when it becomes relavant


def find_shortest_path_with_heap(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    H = HeapPQ(graph)
    return dijkstras(H, graph, source, target)


def find_shortest_path_with_array(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    A = ArrayPQ(graph)
    return dijkstras(A, graph, source, target)

def dijkstras(pq, graph, source, target):
    distance = {}
    previous = {}
    for node in graph:
        distance[node] = math.inf
        previous[node] = None

    distance[source] = 0
    pq.setPriority(source, 0) # doesn't count

    while not pq.isEmpty(): # bool

        current_node = pq.deleteMin() # Olog(V)

        if current_node == target: # O(1)
            break

        for away_edge in graph[current_node]: # O(E)
            weight = graph[current_node][away_edge] # O(1)
            current_distance = distance[current_node] + weight # O(1)

            if distance[away_edge] > current_distance: # constant
                distance[away_edge] = current_distance
                previous[away_edge] = current_node
                pq.decrease_key(away_edge, current_distance) #

    # need to rework this logic lol

    return_previous = []
    previous_node = target
    return_previous.append(target)
    while previous_node != source:
        return_previous.append(previous[previous_node])
        previous_node = previous[previous_node]

    return_previous.reverse()
    return return_previous, distance[target]  # something like that



