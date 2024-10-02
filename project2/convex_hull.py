# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
#from unittest.mock import right

from venv import create

# once I figure out constructors its OVER for you fetchers

import Point

import random

# what if, hear me out, hull is just a list of points. thats it. none of this class business.

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    pointsButAsActualPoints = makePoints(points) # this has a time complexity of O(n)

    full_hull = create_hull(pointsButAsActualPoints) # this is supposed to be O(nlog(n)) but I think I did something wrong.


    points_list = []
    for point in full_hull: # this is also worst case O(n), where every point gets used in the final hull
        newPoint = point.returnX(), point.returnY()
        points_list.append(newPoint)

    return points_list


def create_hull(hull):

    our_median = median(hull) # according to the class notes, this has an average case of O(n), but a worst case of O(n)
    leftList = []
    rightList = []
    left_hull = None
    right_hull = None


    for point in hull: # should return the actual list # O(n) time
        if point.returnX() < our_median.returnX():
            leftList.append(point)
        else:
            rightList.append(point)

    if len(leftList) > 1:
        newLeftHull = buildAHull(leftList, 1)
        left_hull = create_hull(newLeftHull)

    if len(rightList) > 1:
        newRightHull = buildAHull(rightList, 1)
        right_hull = create_hull(newRightHull)


    if not left_hull:
        left_hull = formalizeHull(leftList) # if we don't have a hull, make one. O(n)
    if not right_hull:
        right_hull = formalizeHull(rightList)

    return joinHull(left_hull, right_hull)



def joinHull(leftHull, rightHull):
    leftHead = getRightMost(leftHull) # returns the leftmost point of the hull
    rightHead = getLeftMost(rightHull) # returns the rightmost point of the hull

    L1,R1 = find_upper_tangent(leftHead, rightHead)
    L2,R2 = find_lower_tangent(leftHead, rightHead)

    L1.setCL(R1)
    R1.setCC(L1)

    L2.setCC(R2)
    R2.setCL(L2)

    new_hull = buildAHull(L1, None)
    return new_hull


def formalizeHull(listOfPoints):

    if len(listOfPoints) == 1:
        listOfPoints[0].setCC(listOfPoints[0])
        listOfPoints[0].setCL(listOfPoints[0])

        new_hull = buildAHull(listOfPoints[0], None)
        return new_hull# create a hul from this point


def median(S): # hull!
    # just copying the pseducode given on the slides
    return selection(S, (len(S)//2))


def selection(S, k):

    Sl = []
    Sr = []
    Sv = []
    # need a random pivot v. there are better ways to pick it. I am not going to do that.

    v = (S[random.randint(0, len(S)-1)])


    # choose a random pivot
    for i in range(len(S)):
        if S[i].returnX() < v.returnX(): # make sure this is returning again
            Sl.append(S[i])
        if S[i].returnX() == v.returnX():
            Sv.append(S[i])
        if S[i].returnX() > v.returnX():
            Sr.append(S[i])

    if k < len(Sl):
        return selection(Sl, k)
    if k < (len(Sl) + len(Sv)):
        return v
    else:
    #if k > (len(Sl) + len(Sv)): # for whatever reason I need to make this an else statement or it bricks.
        return selection(Sr, (k - len(Sl) - len(Sv)))


def find_upper_tangent(L,R): # returns line L,R where R is now clockwise of L
    done = False
    while not done:
        done = True

        while L.returnCC() is not None and slope(L.returnCC(), R) < slope(L, R):
            L = L.returnCC()
            done = False


        while R.returnCL() is not None and slope(L, R.returnCL()) > slope(L, R):
            R = R.returnCL()
            done = False
    return L,R


def find_lower_tangent(L,R):
    done = False
    while not done:
        done = True

        while L.returnCL() is not None and slope(L.returnCL(), R) > slope(L, R):
            L = L.returnCL()
            done = False

        while R.returnCC() is not None and slope(L, R.returnCC()) < slope(L, R):
            R = R.returnCC()
            done = False

    return L,R # once again this is the fetcher that we need


def slope(L : Point,R : Point):
    top = R.returnY() - L.returnY()
    bottom = R.returnX() - L.returnX()
    return (top / bottom)


def makePoints(points):
    realPoints = []
    for point in points:
        newPoint = Point.Point(point[0], point[1], point, point)
        newPoint.setCC(point)
        newPoint.setCL(point)
        realPoints.append(newPoint)
    return realPoints


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






def buildAHull(points_list, list):
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
        #point.check()

        while clockWiseStartPoint != None and not clockWiseStartPoint.returnChecked():
            clockWiseStartPoint.check()
            hull.append(clockWiseStartPoint)
            clockWiseStartPoint = clockWiseStartPoint.returnCL()


        while counterClockWiseStartPoint != None and not counterClockWiseStartPoint.returnChecked():
            counterClockWiseStartPoint.check()
            hull.append(counterClockWiseStartPoint)
            counterClockWiseStartPoint = counterClockWiseStartPoint.returnCC()

    resetChecks(hull)
    return hull




def resetChecks(hull):
    for point in hull:
        point.unCheck()

