import math

from dataStructure import dataStructure


def test_lowest_cost_matrix_simple():
    matrix_initial = [
        [math.inf, 8, 12, 4],
        [3, math.inf, 7, 1],
        [2, 6, math.inf, 4],
        [math.inf, 3, 5, math.inf]
    ]
    matrix_final = [
        [math.inf, 4, 6, 0],
        [2, math.inf, 4, 0],
        [0, 4, math.inf, 2],
        [math.inf, 0, 0, math.inf]
    ]
    currentObjcet = dataStructure(matrix_initial, 0, [0])
    new_matrix, cost = currentObjcet.create_lowest_cost_matrix()

    assert new_matrix == matrix_final
    assert cost == 12

def test_lowest_cost_matrix_complex():
    state1 = [
        [math.inf, 1, math.inf, 0, math.inf],
        [math.inf, math.inf, 1, math.inf, 0],
        [math.inf, 0, math.inf, 1, math.inf,],
        [math.inf, 0, 0, math.inf, 6],
        [0, math.inf, math.inf, 9, math.inf],
        ]
    cost1 = 21


    state2 = [
        [math.inf, math.inf, math.inf, math.inf, math.inf],
        [math.inf, math.inf, 1, math.inf, 0],
        [math.inf, 0, math.inf, math.inf, math.inf,],
        [math.inf, 0, 0, math.inf, 6],
        [0, math.inf,math.inf,math.inf,math.inf],
    ]
    cost2 = 21

    newObject = dataStructure(state1, 21, [0])
    newLowestCostMatrix, newCost = newObject.create_lowest_cost_matrix(0,3)
    object2 = dataStructure(newLowestCostMatrix, newCost, [0])

    assert state2 == newLowestCostMatrix
    assert cost2 == newCost

    newNewLowestCostMatrix, newNewCost = object2.create_lowest_cost_matrix(3,2)


    assert newNewCost == 21