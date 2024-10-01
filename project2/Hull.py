import Point

class Hull: # literally just list of points but I like having it as a class :)

    hull = []

    def __init__(self, points_list, list = None):
        self.hull.clear()
        if list is not None:

            for point in points_list:
                Point.Point(point[0], point[1], point, point)
                self.hull.append(point)


        else:
            self.hull.clear()
            point = points_list

            newPointsList = []
            clockWiseStartPoint = point
            counterClockWiseStartPoint = point.returnCC

            self.hull.append(point)
            point.check()

            while clockWiseStartPoint != None and not point.returnChecked():
                point.check()
                self.hull.append(point)
                point = point.returnCL()


            while counterClockWiseStartPoint != None and not point.returnChecked():
                point.check()
                self.hull.append(Point)
                point = point.returnCC()


        # creates a new hull from the connected points and returns that hull
        # this is going to be black voodoo magic.


    def __add__(self, Point):
        self.hull.append(Point)

    def __len__(self):
        return len(self.hull)

    def createList(self): # makes a list of non points (array) to return to finalize stuff
        newList = []
        for point in self.hull:
            newList.append(point)
        # bleh bleh bleh # this is probably wrong
        return newList

    def resetChecks(self):
        for point in self.hull:
            point.unCheck()

    def __getitem__(self, index):
        return self.hull[index]



