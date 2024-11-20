
class dataStructure:
    def __init__(self, lowestCostMatrix, currentCost, currentPath, priority=None):
        self.lowestCostMatrix = lowestCostMatrix
        self.currentCost = currentCost
        self.current_path = currentPath
        self.priority = priority

    def get_latest_node(self):
        return self.current_path

    def get_lowest_cost_matrix(self):
        return self.lowestCostMatrix

    def get_current_cost(self):
        return self.currentCost

    def __lt__(self, other):
        return self.priority < other.priority