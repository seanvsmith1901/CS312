import math

def find_shortest_path_with_heap(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:

    distance = {}
    previous = {}
    for node in graph:
        distance[node] = math.inf
        previous[node] = None

    distance[source] = 0

    H = HeapPQ(graph) # should use the distances as keys, we shall see. I don't think this is workign the way that I want it to.

    while H: # just adding a comment to force changes lol
        current_node = H.__next__()

        for away_edge in graph[current_node]:

            weight = graph[current_node][away_edge]

            if distance[away_edge] > distance[current_node] + weight:
                distance[away_edge] = distance[current_node] + weight
                previous[away_edge] = current_node
                H.set_priority(away_edge, weight)



    # this works just fine, not a lot going on here.
    return_previous = []
    previous_node = target
    return_previous.append(target)

    while previous_node != source:
        return_previous.append(previous[previous_node])
        previous_node = previous[previous_node]

    return_previous.reverse()
    return return_previous, distance[target] # something like that



def find_shortest_path_with_array(
        graph: list[list[float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    distance = {}
    previous = {}
    for node in graph:
        distance[node] = math.inf
        previous[node] = None

    distance[source] = 0

    A = ArrayPQ(graph)  # should use the distances as keys, we shall see. I don't think this is workign the way that I want it to.

    while A:
        current_node = A.__next__()

        if current_node == target:
            break

        for away_edge in graph[current_node]:
            weight = graph[current_node][away_edge]

            if distance[away_edge] > distance[current_node] + weight:
                distance[away_edge] = distance[current_node] + weight
                previous[away_edge] = current_node
                A.set_priority(away_edge, weight)

    # need to rework this logic lol

    return_previous = []
    previous_node = target
    return_previous.append(target)
    while previous_node != source:
        return_previous.append(previous[previous_node])
        previous_node = previous[previous_node]

    return_previous.reverse()
    return return_previous, distance[target]  # something like that






