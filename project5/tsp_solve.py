import math
import random
import queue
from queue import PriorityQueue

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

import copy

from dataStructure import *
# force push I like this one

def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    currentNode = 0 # keep track of where we are
    # so for the adjacency matrix, go through at that i and then look for the lowest value (that isn't itself) and then store it and consult that node
    # if the lowest cost is inf, then we are fetched, we can prune that tree and we can try again with a differnet one.
    # also check that for every node that you get on, taht youc an still get off. If you no longer can get off, prune it!
    # cast it into the fire! destroy it!


    while True:
        if timer.time_out():
            return stats

        visited = set()

        stack = [currentNode]
        tour = []
        while stack:
            node = stack[-1]
            if node not in visited:
                visited.add(node)
                currentMin = math.inf
                nextNode = None
                for i in range(len(edges[node])):
                    if i != node and i not in visited: # make sure we avoid the null
                        n_nodes_expanded += 1
                        if edges[node][i] < currentMin:
                            currentMin = edges[node][i]
                            nextNode = i
                        else:
                            n_nodes_pruned += 1

                stack.pop()
                if nextNode is not None:
                    stack.append(nextNode)

                tour.append(node)



        currentNode += 1

        if len(tour) == len(edges):
            cost = score_tour(tour, edges)

            if math.isinf(cost):
                n_nodes_pruned += 1
                cut_tree.cut(tour)
                currentNode += 1
                continue


            if stats and cost > stats[-1].score:
                n_nodes_pruned += 1
                cut_tree.cut(tour)

                continue

            stats.append(SolutionStats(
                tour=tour,
                score=cost,
                time=timer.time(),
                max_queue_size=1,
                n_nodes_expanded=n_nodes_expanded,
                n_nodes_pruned=n_nodes_pruned,
                n_leaves_covered=cut_tree.n_leaves_cut(),
                fraction_leaves_covered=cut_tree.fraction_leaves_covered()
            ))

            break # don't forget this fetcher he is very important

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    return stats


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    max_queue_size = 0
    currentNode = 0
    previous = {}
    distance = {}
    cost = {}

    graph = {} # gets me a graph in a way that makes sense
    for i in range(len(edges)):
        for j in range(len(edges)):
            if edges[i][j] != math.inf and i != j:
                if i not in graph:
                    graph[i] = [j]
                else:
                    graph[i].append(j)

    for node in graph:
        distance[node] = math.inf
        previous[node] = None


    while True:
        stack = []
        if timer.time_out():
            return stats

        stack.append([0]) # always start from city 0

        while stack:
            if len(stack) > max_queue_size: # just to check our max size
                max_queue_size = len(stack)

            possible_route = stack.pop()
            node_to_test = possible_route[-1] # looks at the node on the top
            for neighbor in graph.get(node_to_test, []):
                new_route = possible_route.copy() # normal copy seems to work fine here but we might need to change it
                if neighbor not in possible_route:
                    new_route.append(neighbor)
                    if len(new_route) == len(edges):
                        add_stats(new_route, edges, n_nodes_pruned, stats, n_nodes_expanded, cut_tree, timer, max_queue_size)

                    stack.append(new_route)

        break




    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    return stats


def add_stats(tour, edges, n_nodes_pruned, stats, n_nodes_expanded, cut_tree, timer, max_queue_size):
    if len(tour) == len(edges):
        cost = score_tour(tour, edges)

        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            return

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            return # the cost iss greater we don't want him

        if stats:
            if cost < stats[-1].score:  # only add it to stats if it is a lower score
                stats.append(SolutionStats(
                    tour=tour,
                    score=cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
        else:
            stats.append(SolutionStats(
                tour=tour,
                score=cost,
                time=timer.time(),
                max_queue_size=1,
                n_nodes_expanded=n_nodes_expanded,
                n_nodes_pruned=n_nodes_pruned,
                n_leaves_covered=cut_tree.n_leaves_cut(),
                fraction_leaves_covered=cut_tree.fraction_leaves_covered()
            ))



def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    initial_state = copy.deepcopy(edges)

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(initial_state))
    max_queue_size = 0
    current_tour = greedy_tour(edges, timer)
    BSSF = current_tour[0].score # this exists ENTIRELY FOR testing so don't look at it too hard
    add_stats_simple(current_tour[0].tour, stats, BSSF, n_nodes_expanded, n_nodes_pruned, cut_tree, timer, max_queue_size)

    # DO ROWS THEN EDGES FOR THE LOWEST COST EDGES
    #
    lowestCostMatrix, leastCost = create_lowest_cost_matrix(initial_state)

    while True:
        stack = []
        newObject = dataStructure(initial_state, leastCost, [0])
        stack.append(newObject) # always start from city 0

        while stack:
            if len(stack) > max_queue_size: # just to check our max size
                max_queue_size = len(stack)
            if timer.time_out():
                return stats

            newObject = stack.pop()

            current_route = newObject.get_latest_node()
            node_to_test = current_route[-1]

            lowestCostMatrix = newObject.get_lowest_cost_matrix()
            current_cost = newObject.get_current_cost()

            for j in range(len(initial_state)):
                if (lowestCostMatrix[node_to_test][j] != math.inf) and (node_to_test != j) and (j not in current_route): # its an edge we can actually travel to
                    new_cost = lowestCostMatrix[node_to_test][j] + current_cost
                    if new_cost < BSSF:

                        new_route = copy.deepcopy(current_route)
                        new_route.append(j)

                        if len(new_route) == len(lowestCostMatrix):
                            if edges[j][node_to_test] != math.inf:
                                add_stats_simple(new_route, stats, new_cost, n_nodes_expanded, n_nodes_pruned, cut_tree, timer, max_queue_size)
                                BSSF = new_cost
                        else:
                            newLowestCostMatrix = copy.deepcopy(lowestCostMatrix) # I don't want it to edit previous iterations of the matrix
                            newlowestCostMatrix, sum = create_lowest_cost_matrix(newLowestCostMatrix, node_to_test, j, new_cost)
                            if sum < BSSF:

                                newObject = dataStructure(newlowestCostMatrix, sum, new_route)
                                stack.append(newObject)

                    # else we prune him. he does not get to know on the stack.
        break

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    return stats


def add_stats_simple(tour, stats, cost, n_nodes_expanded, n_nodes_pruned, cut_tree, timer, max_queue_size):
    if cost != math.inf:

        if stats:
            if cost < stats[-1].score:  # only add it to stats if it is a lower score
                stats.append(SolutionStats(
                    tour=tour,
                    score=cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
        else:
            stats.append(SolutionStats(
                tour=tour,
                score=cost,
                time=timer.time(),
                max_queue_size=1,
                n_nodes_expanded=n_nodes_expanded,
                n_nodes_pruned=n_nodes_pruned,
                n_leaves_covered=cut_tree.n_leaves_cut(),
                fraction_leaves_covered=cut_tree.fraction_leaves_covered()
            ))


def create_lowest_cost_matrix(lowestCostMatrix, row=None, column=None, newCost=0):

    #updates our cognates (can't take that same edge again)
    if row is not None and column is not None:
        lowestCostMatrix[row][column] = math.inf
        lowestCostMatrix[column][row] = math.inf

        # turns our rows and columns to 0 like we did on the homework
        i = row
        for j in range(len(lowestCostMatrix)):
            lowestCostMatrix[i][j] = math.inf

        i = column
        for j in range(len(lowestCostMatrix)):
            lowestCostMatrix[j][i] = math.inf

    # actually does all the row reduction after we cancel out our rows and columns.
    if newCost == 0:
        sum = 0
    else:
        sum = newCost

    for i in range(len(lowestCostMatrix)): # this does the i portions
        lowestNumber = math.inf
        for j in range(len(lowestCostMatrix)):
            if lowestCostMatrix[i][j] < lowestNumber and i != j:
                lowestNumber = lowestCostMatrix[i][j]

        if lowestNumber != math.inf:
            sum += lowestNumber

        for j in range(len(lowestCostMatrix)):
            if lowestCostMatrix[i][j] != math.inf and i != j:
                lowestCostMatrix[i][j] -= lowestNumber

    for j in range(len(lowestCostMatrix)):
        lowestNumber = math.inf
        for i in range(len(lowestCostMatrix)):
            if lowestCostMatrix[i][j] < lowestNumber and i != j:
                lowestNumber = lowestCostMatrix[i][j]

        if lowestNumber != math.inf:
            sum += lowestNumber

        for i in range(len(lowestCostMatrix)):
            if lowestCostMatrix[i][j] != math.inf and i != j:
                lowestCostMatrix[i][j] -= lowestNumber

    return lowestCostMatrix, sum


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    initial_state = copy.deepcopy(edges)

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(initial_state))
    max_queue_size = 0

    BSSF = (greedy_tour(initial_state, timer))[0].score
    lowestCostMatrix, leastCost = create_lowest_cost_matrix(initial_state)

    while True:
        heap = PriorityQueue()

        newObject = dataStructure(initial_state, leastCost, [0], math.inf)
        heap.put(newObject) # we are allowed to start from other cities but I don't want to mess with that yet.

        while heap:
            if heap.qsize() > max_queue_size: # just to check our max size
                max_queue_size = heap.qsize()
            if timer.time_out():
                return stats

            newObject = heap.get()

            current_cost = newObject.get_current_cost() # prune if the current cost is greater than the known lower bound

            if current_cost < BSSF: # make sure we are activley pruning what we pull of off the heap as well, just in case.
                current_route = newObject.get_latest_node()
                node_to_test = current_route[-1]
                lowestCostMatrix = newObject.get_lowest_cost_matrix()

                for j in range(len(lowestCostMatrix)):
                    if (lowestCostMatrix[node_to_test][j] != math.inf) and (node_to_test != j) and (j not in current_route): # its an edge we can actually travel to
                        new_cost = lowestCostMatrix[node_to_test][j] + current_cost
                        if new_cost < BSSF: # if the child has a new lower cost than the known best route

                            new_route = copy.deepcopy(current_route)
                            new_route.append(j)
                            if len(new_route) == len(lowestCostMatrix): # test for end edge cases
                                if edges[j][node_to_test] != math.inf:
                                    add_stats_simple(new_route, stats, new_cost, n_nodes_expanded, n_nodes_pruned, cut_tree,
                                                     timer, max_queue_size)
                                    BSSF = new_cost
                            else: # its a new, lower cost than our current known best.
                                newLowestCostMatrix = copy.deepcopy(lowestCostMatrix)  # I don't want it to edit previous iterations of the matrix
                                newlowestCostMatrix, sum = create_lowest_cost_matrix(newLowestCostMatrix, node_to_test, j, new_cost)
                                if sum < BSSF:
                                    priority = sum * (len(newlowestCostMatrix) - len(new_route))
                                    newObject = dataStructure(newlowestCostMatrix, sum, new_route, priority)  # new cost for prio?
                                    heap.put(newObject)

        break

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    return stats
