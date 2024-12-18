import math
import copy

class dataStructure:
    def __init__(self, lowestCostMatrix, lowerBound, currentPath, priority=None):
        self.lowestCostMatrix = lowestCostMatrix
        self.lowerBound = lowerBound
        self.current_path = currentPath
        self.priority = priority

    def get_latest_node(self):
        return self.current_path[-1]

    def get_lowest_cost_matrix(self):
        return self.lowestCostMatrix

    def get_lower_bound(self):
        return self.lowerBound

    def __lt__(self, other):
        if self.priority == None:
            return self.currentCost < other.currentCost
        else:
            return self.priority < other.priority

    def get_tour(self):
        return self.current_path

    def set_lower_bound(self, lowerBound):
        self.lowerBound = lowerBound

    def create_lowest_cost_matrix(self, row=None, column=None):

        lowestCostMatrix = copy.deepcopy(self.lowestCostMatrix)
        sum = 0
        sum += self.lowerBound


        # updates our cognates (can't take that same edge again)
        if row is not None and column is not None:
            sum += lowestCostMatrix[row][column]
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

        for i in range(len(lowestCostMatrix)):  # this does the i portions
            if i not in self.current_path:
                lowestNumber = math.inf
                for j in range(len(lowestCostMatrix)):
                    if lowestCostMatrix[i][j] < lowestNumber and i != j:
                        lowestNumber = lowestCostMatrix[i][j]

                sum += lowestNumber

                for j in range(len(lowestCostMatrix)):
                    if lowestCostMatrix[i][j] != math.inf and i != j:
                        lowestCostMatrix[i][j] -= lowestNumber

        for j in range(len(lowestCostMatrix)):
            if j not in self.current_path:
                lowestNumber = math.inf
                for i in range(len(lowestCostMatrix)):
                    if lowestCostMatrix[i][j] < lowestNumber and i != j:
                        lowestNumber = lowestCostMatrix[i][j]


                sum += lowestNumber

                for i in range(len(lowestCostMatrix)):
                    if lowestCostMatrix[i][j] != math.inf and i != j:
                        lowestCostMatrix[i][j] -= lowestNumber

        return lowestCostMatrix, sum

