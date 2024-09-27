import Point

class Hull: # literally just list of points but I like having it as a class :)

    def __init__(self):
        self.hull = []

    def __init__(self, points_list):
        for point in points_list:
            self.__add__(self, point)

    def __init__(self, point):
        # creates a new hull from the connected points and returns that hull
        # this is going to be black voodoo magic.


    def __add__(self, Point):
        self.hull.append(Point)

    def __len__(self):
        return len(self.hull)

    def __createList__(self): # makes a list of non points (array) to return to finalize stuff
        # bleh bleh bleh
        return self

