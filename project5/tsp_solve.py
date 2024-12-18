import heapq
import math
import random
import queue
from queue import PriorityQueue

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver, score_partial_tour
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
    BSSF = math.inf
    stack = []
    stack.append([0])  # always start from city 0

    while stack:

        if timer.time_out(): # get rid of this when debugging i think
          return stats

        if len(stack) > max_queue_size: # just to check our max size
            max_queue_size = len(stack)

        possible_route = stack.pop()
        node_to_test = possible_route[-1] # looks at the node on the top
        for j in range(len(edges)):
            if (j != node_to_test) and (edges[node_to_test][j] != math.inf) and (j not in possible_route):
                n_nodes_expanded += 1
                new_route = copy.deepcopy(possible_route)
                new_route.append(j)
                new_cost = score_partial_tour(new_route, edges) # I borrow him :)
                if new_cost < BSSF:
                    full_cost = score_tour(new_route, edges)
                    if len(new_route) == len(edges):
                        if full_cost < BSSF:
                            BSSF = full_cost
                            add_stats(new_route, edges, n_nodes_pruned, stats, n_nodes_expanded, cut_tree, timer, max_queue_size)
                    else:
                        stack.append(new_route)
                else:
                    n_nodes_pruned += 1
            else:
                cut_tree.cut(possible_route)



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


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    initial_state = copy.deepcopy(edges)

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(initial_state))
    max_queue_size = 0
    # get bssf from greedy
    current_tour = greedy_tour(edges, timer)
    BSSF = current_tour[0].score
    # create an object to throw on stack
    currentObject = dataStructure(initial_state, 0, [0])
    newLowestCostMatrix, lowerBound = currentObject.create_lowest_cost_matrix()
    newObject = dataStructure(newLowestCostMatrix, lowerBound, [0])
    # create stack and throw stuff on it
    stack = []
    stack.append(newObject) # always start from city 0


    while stack: # the search begins
        if len(stack) > max_queue_size: # just to check our max size
            max_queue_size = len(stack)
        if timer.time_out():
            break

        # get most recent object
        newObject = stack.pop()
        currentCost = newObject.get_lower_bound()


        # check for completeness
        if len(newObject.current_path) == len(initial_state):
            BSSF = check_complete(initial_state, newObject, stats, timer, max_queue_size, n_nodes_expanded, n_nodes_pruned, cut_tree, BSSF, stack)

        # not complete, check for cost
        if currentCost < BSSF: # make sure we are activley pruning what we pull of off the heap as well, just in case.
            n_nodes_expanded, n_nodes_pruned, BSSF = expansion(newObject, initial_state, stack, n_nodes_expanded, n_nodes_pruned, BSSF, cut_tree)
        else:
            cut_tree.cut(newObject.current_path) # cost to much, cut him out


    # if no solutions or our solution is worse than our greedy solution, throw him on.
    if not stats or stats[-1].score > current_tour[0].score:
        return [SolutionStats(
            current_tour[0].tour,
            current_tour[0].score,
            timer.time(),
            max_queue_size,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    return stats

def expansion(newObject, initial_state, stack, n_nodes_expanded, n_nodes_pruned, BSSF, cut_tree):
    for j in range(len(initial_state)):  # expansion for all neighbors of current neighbor
        current_route = newObject.current_path
        node_to_test = current_route[-1]
        lowestCostMatrix = newObject.get_lowest_cost_matrix()
        # make sure neighbor is real and exists
        if (lowestCostMatrix[node_to_test][j] != math.inf) and (node_to_test != j) and (
                j not in current_route and node_to_test in current_route):  # its an edge we can actually travel to
            # ready up for creating the lowest cost matrix
            thisObject = copy.deepcopy(newObject)
            thisObject.current_path.append(j)
            newLowestMatrix, new_lower_bound = thisObject.create_lowest_cost_matrix(node_to_test, j)

            if new_lower_bound < BSSF:  # if the child has a new lower cost than the known best route
                thisObject = copy.deepcopy(newObject)
                thisObject.set_lower_bound(new_lower_bound)

                new_route = copy.deepcopy(newObject.current_path)
                new_route.append(j)
                n_nodes_expanded += 1
                # creates new object, puts it on stack
                newObjectPath = dataStructure(newLowestMatrix, new_lower_bound, new_route)  # new cost for prio?
                stack.append(newObjectPath)
            else:
                n_nodes_pruned += 1 # we can prune that definitely real node
                cut_tree.cut(thisObject.current_path) # cut that real route out
        # can't do anything here because that node might not exist.

    return n_nodes_expanded, n_nodes_pruned, BSSF


# harder better faster stronger
def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    initial_state = copy.deepcopy(edges)

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(initial_state))
    max_queue_size = 0

    current_tour = greedy_tour(edges, timer)
    BSSF = current_tour[0].score
    starting_node = current_tour[0].tour[-1]

    currentObject = dataStructure(initial_state, 0, [starting_node])
    newLowestCostMatrix, newCost = currentObject.create_lowest_cost_matrix()
    newObject = dataStructure(newLowestCostMatrix, newCost, [starting_node])

    heap = [] # biggest difference - use a heap instead of stack list
    heapq.heappush(heap, newObject) # on he goes


    while heap:
        if len(heap) > max_queue_size: # just to check our max size
            max_queue_size = len(heap)
        if timer.time_out(): break # failsafe

        # get most recent object
        newObject = heapq.heappop(heap)
        currentCost = newObject.get_lower_bound()


        # check for completeness
        if len(newObject.current_path) == len(initial_state):
            max_queue_size = len(heap)
            BSSF = check_complete(initial_state, newObject, stats, timer, max_queue_size, n_nodes_expanded, n_nodes_pruned, cut_tree, BSSF, heap)

        # not complete, check for cost
        if currentCost < BSSF: # make sure we are activley pruning what we pull of off the heap as well, just in case.
            n_nodes_expanded, n_nodes_pruned, BSSF = expansionPriorityQueue(newObject, initial_state, heap, n_nodes_expanded, n_nodes_pruned, BSSF, cut_tree)
        else:
            cut_tree.cut(newObject.current_path) # wasn't useful, cut him out of our lives

    if not stats or stats[-1].score > current_tour[0].score:
        return [SolutionStats(
            current_tour[0].tour,
            current_tour[0].score,
            timer.time(),
            max_queue_size,
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




def check_complete(initial_state, newObject, stats, timer, max_queue_size, n_nodes_expanded, n_nodes_pruned, cut_tree, BSSF, heap):
    if initial_state[newObject.get_latest_node()][0] != math.inf:  # test for end edge cases
        max_queue_size = len(heap)
        add_stats_simple(newObject.current_path, stats, score_tour(newObject.current_path, initial_state), n_nodes_expanded,
                         n_nodes_pruned, cut_tree,
                         timer, max_queue_size)
        BSSF = newObject.get_lower_bound()  # hopefully this works

    else:
        cut_tree.cut(newObject.current_path)
        n_nodes_pruned += 1
    return BSSF



def expansionPriorityQueue(newObject, initial_state, heap, n_nodes_expanded, n_nodes_pruned, BSSF, cut_tree):
    for j in range(len(initial_state)):  # expansion for ever nieghbor
        current_route = newObject.current_path
        node_to_test = current_route[-1]
        lowestCostMatrix = newObject.get_lowest_cost_matrix()
        # make sure neighbor is real and exists
        if (lowestCostMatrix[node_to_test][j] != math.inf) and (node_to_test != j) and (
                j not in current_route and node_to_test in current_route):  # its an edge we can actually travel to
            # prepare and make new lower bound
            thisObject = copy.deepcopy(newObject)
            thisObject.current_path.append(j)
            newLowestMatrix, new_lower_bound = thisObject.create_lowest_cost_matrix(node_to_test, j)

            if new_lower_bound < BSSF:  # if the child has a still valid lower bound
                thisObject = copy.deepcopy(newObject)
                thisObject.set_lower_bound(new_lower_bound)

                new_route = copy.deepcopy(newObject.current_path)
                new_route.append(j)
                n_nodes_expanded += 1
                #explained better in paper, but we want to create shelves and prune aggresively.
                priority = new_lower_bound + 10 * (len(initial_state) - len(new_route))
                # on you go new object
                newOjectPath = dataStructure(newLowestMatrix, new_lower_bound, new_route, priority)
                heapq.heappush(heap, newOjectPath)
            else:
                n_nodes_pruned += 1 # was a real neighbor, but not useful. prune and cut route.


    return n_nodes_expanded, n_nodes_pruned, BSSF






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


