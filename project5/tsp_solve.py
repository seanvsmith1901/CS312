import math
import random

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


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
                        if edges[node][i] < currentMin:
                            currentMin = edges[node][i]
                            nextNode = i

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
            possible_route = stack.pop()
            node_to_test = possible_route[-1] # looks at the node on the top
            for neighbor in graph.get(node_to_test, []):
                new_route = possible_route.copy()
                if neighbor not in possible_route:
                    new_route.append(neighbor)
                    if len(new_route) == len(edges):
                        add_stats(new_route, edges, n_nodes_pruned, stats, n_nodes_expanded, cut_tree, timer)

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


def add_stats(tour, edges, n_nodes_pruned, stats, n_nodes_expanded, cut_tree, timer):
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
                    max_queue_size=1,
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
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    currentNode = 0
    previous = {}
    distance = {}
    cost = {}

    # DO ROWS THEN EDGES FOR THE LOWEST COST EDGES
    lowestCostMatrix = [[math.inf for _ in range(len(edges))]for _ in range(len(edges))]

    sum = 0
    for i in range(len(edges)): # this does the i portions
        lowestNumber = math.inf
        for j in range(len(edges)):
            if lowestCostMatrix[i][j] < lowestNumber:
                lowestNumber = lowestCostMatrix[i][j]
        sum += lowestNumber
        for j in range(len(edges)):
            lowestCostMatrix[i][j] -= lowestNumber

    for j in range(len(edges)):
        lowestNumber = math.inf
        for i in range(len(edges)):
            if lowestCostMatrix[i][j] < lowestNumber:
                lowestNumber = lowestCostMatrix[i][j]
        sum += lowestNumber
        for j in range(len(edges)):
            lowestCostMatrix[i][j] -= lowestNumber


    #OK SO YOU DO WEIRD STUFF
    # Once you have left node 1, you will never use it again, so we can make a bunch of stuff infinity
    # and you can delete all teh ingoing states from 2 (assuming we are going frmo 1 to 2)

    #then update your rows and columns
    # so make that fetcher a function and make it possible to throw him in (we need to be able to
    # so just update teh whole matrix to find the "new" lower cost
    # so turn taht above thing into a function and go from there

    # and you will need to store those reduced cost matricies for different states (I suggest doing a dictinoary IG, or IG we could put it on the stack. that owuld be fetched)
    # partial path, cost, matrix (need all 3 of these to know where we are adn where we are going)
    # we infinitize the row 1 (becuase we leave row 1) and we finitize column 3 (because we netered row 3)

    # after we update the reduced cost matrix, update the max cost by finding the lowest possible cost on every node that is left
    # if the lowest cost is infinity on any of the nodes, break and don't add him to teh stack becuase he is NOT worht it.

    # update the best solution adn make sure that the best cost is still teh lowest.
    # once the queue is empty we are retuning optimal
    # branch and bound will also give us a timer and we will be taking advantage of that.

    # we need a way to KNOW which rows I carea bout and which ones I dont
    # if we get an infity of a row or a column that I care about, thats a problem
    # but if i get a real answer we can keep going.



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
            possible_route = stack.pop()
            node_to_test = possible_route[-1] # looks at the node on the top
            for neighbor in graph.get(node_to_test, []):
                new_route = possible_route.copy()
                if neighbor not in possible_route:
                    new_route.append(neighbor)
                    if len(new_route) == len(edges):
                        add_stats(new_route, edges, n_nodes_pruned, stats, n_nodes_expanded, cut_tree, timer)

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


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    # S = stack.pop()
    # wrong! use a priority queue and maybe change your starting node. Play with teh priority.
    # do depth first search with a priority queue on the children that we do
    # how can we guide it to pick better options most of the time?
    # DO NOT USE LOWER BOUND AS PRIORITY QUEUE OTHERWISE YOU WILL NEVER FIND AN ANSWER BETTER THAN YOUR GREEDY ANSWER.
    # the goal is always better than greedy.
    # how do I want to set my priority queue?
    # (something something A* something something)


    return []
