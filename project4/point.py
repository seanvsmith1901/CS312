from math import inf

class point:
    def __init__(self, i=0, j=0, cost=inf, previous=None):
        self.i = i
        self.j = j
        self.cost = cost
        self.previous = previous

    def set_previous(self, previous):
        self.previous = previous

    def return_cost(self):
        return self.cost

    def __str__(self):
        return self.cost