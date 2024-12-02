def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    initial_state = copy.deepcopy(edges)

    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(initial_state))
    max_queue_size = 0

    current_tour = greedy_tour(edges, timer)
    BSSF = current_tour[0].score

    currentObject = dataStructure(initial_state, 0, [0], 0)
    newLowestCostMatrix, newCost = currentObject.create_lowest_cost_matrix()
    newObject = dataStructure(newLowestCostMatrix, newCost, [0], 0)

    stack = PriorityQueue()
    stack.put(newObject)  # always start from city 0


    while stack:
        if stack.qsize() > max_queue_size:  # just to check our max size
            max_queue_size = stack.qsize()
        if timer.time_out(): return

        # get most recent object
        if stack.queue:
            newObject = stack.queue.pop()
            currentCost = newObject.get_current_cost()
        else:
            break

        # check for completeness
        if len(newObject.current_path) == len(initial_state):
            BSSF = check_complete(initial_state, newObject, stats, timer, max_queue_size, n_nodes_expanded,
                                  n_nodes_pruned, cut_tree, BSSF)

        # not complete, check for cost
        if currentCost < BSSF:  # make sure we are activley pruning what we pull of off the heap as well, just in case.
            expansionPriorityQueue(newObject, stack, initial_state, max_queue_size, n_nodes_expanded, n_nodes_pruned, cut_tree, BSSF)


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


def expansionPriorityQueue(newObject, heap, initial_state, max_queue_size, n_nodes_expanded, n_nodes_pruned, cut_tree, BSSF):
    children_to_add = []
    for j in range(len(initial_state)):

        current_route = newObject.current_path
        node_to_test = current_route[-1]
        lowestCostMatrix = newObject.get_lowest_cost_matrix()


        if (lowestCostMatrix[node_to_test][j] != math.inf) and (node_to_test != j) and (
                j not in current_route):  # its an edge we can actually travel to
            new_cost = lowestCostMatrix[node_to_test][j] + newObject.get_current_cost()


            if new_cost < BSSF:  # if the child has a new lower cost than the known best route
                thisObject = copy.deepcopy(newObject)
                thisObject.set_current_cost(new_cost) # should update the cost for this object only

                new_route = thisObject.current_path
                new_route.append(j)
                newLowestMatrix, newCost = thisObject.create_lowest_cost_matrix(node_to_test, j)
                priority = newCost + (10 * (len(newLowestMatrix) - len(new_route)))
                possibleRoute = dataStructure(newLowestMatrix, newCost, new_route, priority)  # new cost for prio?
                children_to_add.append(possibleRoute)

    children_to_add.sort()
    for i in range(min(2, len(children_to_add))):
        heap.put(children_to_add[i])