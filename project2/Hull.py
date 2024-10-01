import Point

class Hull: # literally just list of points but I like having it as a class :)

    def __init__(self, points_list, list = None):
        hull = []

        if list is not None:

            for point in points_list:
                Point.Point(point[0], point[1], point, point)
                hull.append(point)


        else:
            point = points_list

            newPointsList = []
            clockWiseStartPoint = point.returnCL()
            counterClockWiseStartPoint = point.returnCC()

            hull.append(point)
            point.check()

            while clockWiseStartPoint != None and not clockWiseStartPoint.returnChecked():
                clockWiseStartPoint.check()
                hull.append(clockWiseStartPoint)
                clockWiseStartPoint = clockWiseStartPoint.returnCL()


            while counterClockWiseStartPoint != None and not counterClockWiseStartPoint.returnChecked():
                counterClockWiseStartPoint.check()
                hull.append(counterClockWiseStartPoint)
                counterClockWiseStartPoint = counterClockWiseStartPoint.returnCC()


        # creates a new hull from the connected points and returns that hull
        # this is going to be black voodoo magic.


    def __add__(hull, point):
        hull.append(point)

    def __len__(hull):
        size = 0
        for point in hull.createList():
            size += 1

        return size

    def createList(hull): # makes a list of non points (array) to return to finalize stuff
        newList = []
        for point in hull:
            newList.append(point)
        # bleh bleh bleh # this is probably wrong
        return newList

    def resetChecks(hull):
        for point in hull:
            point.unCheck()

    def __getitem__(hull, index):
        return hull[index]

    def getLeftMost(hull):
        leftMost = hull[0]
        for point in hull:
            if point.returnX() < leftMost.returnX():
                leftMost = point
        return leftMost

    def getRightMost(hull):
        getRightMost = hull[0]
        for point in hull:
            if point.returnX() > getRightMost.returnX():
                getRightMost = point
        return getRightMost



