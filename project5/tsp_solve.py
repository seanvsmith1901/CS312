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
        tour = []
        stack = []
        child = False
        if timer.time_out():
            return stats



        stack.append([0]) # always start from city 0
        # pretty sure all of this is wrong
        # use child paths instead


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
                pass  # do nothing
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
    return []


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
