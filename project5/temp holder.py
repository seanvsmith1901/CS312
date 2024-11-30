def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    initial_state = copy.deepcopy(edges)

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(initial_state))
    max_queue_size = 0

    current_tour = greedy_tour(edges, timer)
    BSSF = current_tour[0].score  # this exists ENTIRELY FOR testing so don't look at it too hard
    #add_stats_simple(current_tour[0].tour, stats, BSSF, n_nodes_expanded, n_nodes_pruned, cut_tree, timer, max_queue_size)

    lowestCostMatrix, leastCost = create_lowest_cost_matrix(initial_state)


    heap = PriorityQueue()

    newObject = dataStructure(initial_state, leastCost, [0], math.inf)
    heap.put(newObject) # we are allowed to start from other cities but I don't want to mess with that yet.


    while heap:
        if heap.qsize() > max_queue_size: # just to check our max size
            max_queue_size = heap.qsize()
        if timer.time_out(): return stats

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



    #
    # current_tour = greedy_tour(edges, timer)
    # BSSF = current_tour[0].score  # this exists ENTIRELY FOR testing so don't look at it too hard
    # #add_stats_simple(current_tour[0].tour, stats, BSSF, n_nodes_expanded, n_nodes_pruned, cut_tree, timer, max_queue_size)
    #
    # lowestCostMatrix, leastCost = create_lowest_cost_matrix(initial_state)
    #
    #
    # heap = PriorityQueue()
    #
    # newObject = dataStructure(initial_state, leastCost, [0], math.inf)
    # heap.put(newObject) # we are allowed to start from other cities but I don't want to mess with that yet.
    #
    #
    # while heap:
    #     if heap.qsize() > max_queue_size: # just to check our max size
    #         max_queue_size = heap.qsize()
    #     if timer.time_out(): return stats
    #
    #     newObject = heap.get()
    #
    #     current_cost = newObject.get_current_cost() # prune if the current cost is greater than the known lower bound
    #
    #     if current_cost < BSSF: # make sure we are activley pruning what we pull of off the heap as well, just in case.
    #         current_route = newObject.get_latest_node()
    #         node_to_test = current_route[-1]
    #         lowestCostMatrix = newObject.get_lowest_cost_matrix()
    #
    #         for j in range(len(lowestCostMatrix)):
    #             if (lowestCostMatrix[node_to_test][j] != math.inf) and (node_to_test != j) and (j not in current_route): # its an edge we can actually travel to
    #                 new_cost = lowestCostMatrix[node_to_test][j] + current_cost
    #                 if new_cost < BSSF: # if the child has a new lower cost than the known best route
    #
    #                     new_route = copy.deepcopy(current_route)
    #                     new_route.append(j)
    #                     if len(new_route) == len(lowestCostMatrix): # test for end edge cases
    #                         if edges[j][node_to_test] != math.inf:
    #                             add_stats_simple(new_route, stats, new_cost, n_nodes_expanded, n_nodes_pruned, cut_tree,
    #                                              timer, max_queue_size)
    #                             BSSF = new_cost
    #                     else: # its a new, lower cost than our current known best.
    #                         newLowestCostMatrix = copy.deepcopy(lowestCostMatrix)  # I don't want it to edit previous iterations of the matrix
    #                         newlowestCostMatrix, sum = create_lowest_cost_matrix(newLowestCostMatrix, node_to_test, j, current_cost)
    #                         if sum < BSSF:
    #                             priority = sum * (len(newlowestCostMatrix) - len(new_route))
    #                             newObject = dataStructure(newlowestCostMatrix, sum, new_route, priority)  # new cost for prio?
    #                             heap.put(newObject)

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
