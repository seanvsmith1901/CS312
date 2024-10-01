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
            point = points_list

            newPointsList = []
            clockWiseStartPoint = point.returnCL()
            counterClockWiseStartPoint = point.returnCC()

            self.hull.append(point)
            point.check()

            while clockWiseStartPoint != None and not clockWiseStartPoint.returnChecked():
                clockWiseStartPoint.check()
                self.hull.append(clockWiseStartPoint)
                clockWiseStartPoint = clockWiseStartPoint.returnCL()


            while counterClockWiseStartPoint != None and not counterClockWiseStartPoint.returnChecked():
                counterClockWiseStartPoint.check()
                self.hull.append(counterClockWiseStartPoint)
                counterClockWiseStartPoint = counterClockWiseStartPoint.returnCC()


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

    def getLeftMost(self):
        leftMost = self.hull[0]
        for point in self.hull:
            if point.returnX() < leftMost.returnX():
                leftMost = point
        return leftMost

    def getRightMost(self):
        getRightMost = self.hull[0]
        for point in self.hull:
            if point.returnX() > getRightMost.returnX():
                getRightMost = point
        return getRightMost



