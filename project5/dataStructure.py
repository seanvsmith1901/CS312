
class dataStructure:
    def __init__(self, lowestCostMatrix, currentCost, currentPath):
        self.lowestCostMatrix = lowestCostMatrix
        self.currentCost = currentCost
        self.current_path = currentPath

    def get_latest_node(self):
        return self.current_path

    def get_lowest_cost_matrix(self):
        return self.lowestCostMatrix

    def get_current_cost(self):
        return self.currentCost