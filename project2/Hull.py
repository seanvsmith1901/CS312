import Point

class Hull: # literally just list of points but I like having it as a class :)

    def __init__(self):
        self.hull = []

    def __init__(self, points_list):
        for point in points_list:
            Point.Point(point[0], point[1], None, None)
            self.hull.append(point)

    def __init__(self, point):
        newPointsList = []
        clockWiseStartPoint = point
        counterClockWiseStartPoint = point.returnCC

        while point.returnCC != None and not point.returnChecked():
            point.setChecked(True)
            newPointsList.append(point)
            point = point.returnCL


        while point.returnCL != None and not point.returnChecked():
            point.setChecked(True)
            newPointsList.append(Point)
            point = point.returnCC


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

