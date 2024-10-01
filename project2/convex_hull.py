# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
#from unittest.mock import right

from venv import create

# once I figure out constructors its OVER for you fetchers

import Point
import Hull
import random

# what if, hear me out, hull is just a list of points. thats it. none of this class business.

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    recursions = 0
    pointsButAsActualPoints = makePoints(points) # turns our list of points into a point object with a head and whatnot
    new_hull = pointsButAsActualPoints
    full_hull = create_hull(new_hull, recursions) # I let the AI generate the getItem function IDK why it watned it
    new_list = new_hull
    return new_list


def create_hull(hull, recursions):

    recursions += 1
    print(recursions)
    our_median = hull.at(median(hull)) # median returns the index of the median fetcher rather than teh actual point
    leftList = []
    rightList = []


    for point in hull.createList(): # should return the actual list
        if point.returnX() > our_median.returnX():
            leftList.append(point)
        else:
            rightList.append(point)

    if len(leftList) > 3:
        newLeftHull = Hull.Hull(leftList, 1)
        create_hull(newLeftHull, recursions)

    if len(rightList) > 3:
        newRightHull = Hull.Hull(rightList, 1)
        create_hull(newRightHull, recursions)

    left_hull = formalizeHull(leftList) # i don't think this is creating a new object and IDK why.
    right_hull = formalizeHull(rightList)


    return joinHull(left_hull, right_hull)



def joinHull(leftHull, rightHull):
    leftHead = leftHull.getRightMost() # returns the leftmost point of the hull
    rightHead = rightHull.getLeftMost() # returns the rightmost point of the hull
    L1,R1 = find_upper_tangent(leftHead, rightHead)
    L1.setCL(R1)
    R1.setCC(L1)

    L2,R2 = find_lower_tangent(leftHead, rightHead)
    L2.setCC(R2)
    R2.setCL(L2)

    new_hull = Hull.Hull(L1) # should create a new hull from that list

    return new_hull


def formalizeHull(listOfPoints):
    #new_hull = Hull.Hull(listOfPoints)

    if len(listOfPoints) == 3: # this is the one where we gotta find the leftMost and rightmost lol
        # find leftmost and rightmost and then detremrine if mid is above or below
        leftMost = listOfPoints[0]
        rightMost = listOfPoints[1]
        middle = listOfPoints[2]

        if(listOfPoints[0].returnX() < listOfPoints[1].returnX()) and listOfPoints[0].returnX() < listOfPoints[2].returnX():# if our first point is more left than second point
            leftMost = listOfPoints[0]
        elif((listOfPoints[1].returnX() < listOfPoints[2].returnX()) and (listOfPoints[1].returnX() < listOfPoints[0].returnX())):
            leftMost = listOfPoints[1]
        else:
            leftMost = listOfPoints[2]
        if (listOfPoints[0].returnX() > listOfPoints[1].returnX()) and listOfPoints[0].returnX() > listOfPoints[2].returnX():  # if our first point is more left than second point
            rightMost = listOfPoints[0]
        elif ((listOfPoints[1].returnX() > listOfPoints[2].returnX()) and (listOfPoints[1].returnX() > listOfPoints[0].returnX())):
            rightMost = listOfPoints[1]
        else:
            rightMost = listOfPoints[2]

        middlePoints = []

        for point in listOfPoints:
            middlePoints.append(point)

        middlePoints.remove(leftMost)
        middlePoints.remove(rightMost)
        middle = middlePoints[0]

        if middle.returnY() > leftMost.returnY(): # edge case 1, with a upwards facing triangle
            leftMost.setCL(middle)
            leftMost.setCC(rightMost)
            middle.setCL(rightMost)
            middle.setCC(leftMost)
            rightMost.setCL(leftMost)
            rightMost.setCC(middle)

        else: # edge case 2, with a downwards facing triangle
            leftMost.setCC(middle)
            leftMost.setCL(rightMost)
            middle.setCC(rightMost)
            middle.setCL(leftMost)
            rightMost.setCC(leftMost)
            rightMost.setCL(middle)

        new_hull = Hull.Hull(leftMost)
        return new_hull



    if len(listOfPoints) == 2:
        listOfPoints[0].setCL(listOfPoints[1])
        listOfPoints[1].setCL(listOfPoints[0])

        listOfPoints[0].setCC(listOfPoints[1])
        listOfPoints[1].setCC(listOfPoints[0])

        new_hull = Hull.Hull(listOfPoints[0])
        return new_hull


    if len(listOfPoints) == 1:
        listOfPoints[0].setCC(listOfPoints[0])
        listOfPoints[0].setCL(listOfPoints[0])

        new_hull = Hull.Hull(listOfPoints[0])
        return new_hull# create a hul from this point




def median(S): # hull!
    # just copying the pseducode given on the slides
    return selection(S, (len(S)/2))


def selection(S, k):

    Sl = []
    Sr = []
    Sv = []
    # need a random pivot v. there are better ways to pick it. I am not going to do that.
    v = S.at((random.randint(0, len(S)-1))).returnX()

    # choose a random pivot
    for i in range(len(S)):
        if S[i][0] < v: # make sure this is returning again
            Sl.append(S.at(i))
        if S[i][0] == v:
            Sv.append(S.at(i))
        if S[i][0] > v:
            Sr.append(S.at(i))

    if k < len(Sl):
        return selection(Sl, k)
    if k < len(Sl) + len(Sv):
        return v
    if k > len(Sl) + len(Sv):
        return selection(Sr, k - len(Sl) - len(Sv))


def find_upper_tangent(L,R): # returns line L,R where R is now clockwise of L
    #leftHead = L
    #rightHead = R
    temp = (L,R)
    done = 0
    while not done:
        done = 1
        Temp = (L,R)
        currSlopeL = slope(L, R)
        currSlopeR = slope(L, R)
        while slope(L.returnCC, R) < currSlopeL:
            L = L.returnCC
            currSlopeL = slope(L, R)
            done = 0
        while slope(L, R.returnCL) > currSlopeR:
            R = R.returnCL
            currSlopeR = slope(L,R)
            done = 0

    temp = L,R
    return temp


def find_lower_tangent(L,R):
    #leftHead = L
    #rightHead = R
    temp = (L,R)
    done = 0
    while not done:
        done = 1
        temp = (L,R)
        while slope(L.returnCL, R) > currSlopeL:
            L = L.returnCl
            currSlopeL = slope(L,R)
            done = 0
        while slope(L, R.returnCC) < currSlopeR:
            R = R.returnCC
            currSlopeR = slope(L,R)
            done = 0

    temp = L,R
    return temp # once again this is the fetcher that we need




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






def createHull(point, list):
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