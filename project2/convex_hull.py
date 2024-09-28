# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point
#from unittest.mock import right

from venv import create

# once I figure out constructors its OVER for you fetchers

import Point
import Hull
import random

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:

    pointsButAsActualPoints = makePoints(points) # turns our list of points into a point object with a head and whatnot
    new_hull = Hull.Hull(pointsButAsActualPoints)
    new_hull = create_hull(new_hull) # I let the AI generate the getItem function IDK why it watned it
    new_list = new_hull.create_list()
    return new_list


def create_hull(hull):

    our_median = median(hull)
    leftList = []
    rightList = []

    for point in hull.__createList__(): # should return the actual list
        if point.returnX > our_median.returnX:
            leftList.append(point)
        else:
            rightList.append(point)

    if len(leftList) > 3:
        newHull = Hull.Hull(leftList)
        create_hull(newHull)

    if len(rightList) > 3:
        newHull = Hull.Hull(leftList)
        create_hull(newHull)

    left_hull = formalizeHull(leftList)
    right_hull = formalizeHull(rightList)

    return joinHull(left_hull, right_hull)



def joinHull(leftHull, rightHull):
    L1,R1 = find_upper_tangent(leftHull, rightHull)
    L1.setCL(R1)
    R1.setCC(L1)

    L2,R2 = find_lower_tangent(leftHull, rightHull)
    L2.setCC(R2)
    R2.setCL(L2)

    new_hull = Hull(L1) # should create a new hull from that list

    return new_hull


def formalizeHull(listOfPoints):
    new_hull = Hull(listOfPoints)

    if len(listOfPoints) == 3: # this is the one where we gotta find the leftMost and rightmost lol
        # find leftmost and rightmost and then detremrine if mid is above or below
        leftMost = listOfPoints[0]
        rightMost = listOfPoints[1]
        middle = listOfPoints[2]

        if(listOfPoints[0].returnX < listOfPoints[1].returnX) and listOfPoints[0].returnX < listOfPoints[2].returnX:# if our first point is more left than second point
            leftMost = listOfPoints[0][0]
        elif((listOfPoints[1].returnX < listOfPoints[2].returnX) and (listOfPoints[1].returnX < listOfPoints[0].returnX)):
            leftMost = listOfPoints[1]
        else:
            leftMost = listOfPoints[2]
        if (listOfPoints[0].returnX > listOfPoints[1].returnX) and listOfPoints[0].returnX > listOfPoints[2].returnX:  # if our first point is more left than second point
            rightMost = listOfPoints[0][0]
        elif ((listOfPoints[1].returnX > listOfPoints[2].returnX) and (listOfPoints[1].returnX > listOfPoints[0].returnX)):
            rightMost = listOfPoints[1]
        else:
            rightMost = listOfPoints[2]

        newListOfPoints = listOfPoints.remove(leftMost, rightMost)
        middle = newListOfPoints[0]

        if middle.returnY > leftMost.returnY: # edge case 1, with a upwards facing triangle
            leftMost.setCL(middle)
            leftMost.setCC(rightMost)
            middle.setCC(leftMost)
            middle.SetCL(rightMost)
            rightMost.setCL(leftMost)
            rightMost.setCC(middle)

        else: # edge case 2, with a downwards facing triangle
            leftMost.setCC(middle)
            leftMost.setCL(rightMost)
            middle.setCL(leftMost)
            middle.SetCC(rightMost)
            rightMost.setCC(leftMost)
            rightMost.setCL(middle)

        new_hull = Hull.Hull(leftMost)



    if len(listOfPoints) == 2:
        listOfPoints[0].setCL(listOfPoints[1])
        listOfPoints[1].setCL(listOfPoints[0])

        listOfPoints[0].setCC(listOfPoints[1])
        listOfPoints[1].setCC(listOfPoints[0])

        new_hull = Hull.Hull(listOfPoints[0])


    if len(listOfPoints) == 1:
        listOfPoints[0].setCC(listOfPoints[0])
        listOfPoints[0].setCL(listOfPoints[0])

        new_hull = Hull.Hull(listOfPoints[0]) # create a hul from this point

    return new_hull



def median(S): # hull!
    # just copying the pseducode given on the slides
    return selection(S, len(S)/2)


def selection(S, k):

    Sl = []
    Sr = []
    Sv = []
    # need a random pivot v. there are better ways to pick it. I am not going to do that.
    v = S[(random.randint(0, len(S)-1))][0]

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
    top = R.returnY - L.returnY
    bottom = R.returnX - L.returnX

    return top / bottom

def makePoints(points):
    realPoints = []
    for point in points:
        newPoint = Point(point[0], point[1], point, point)
        realPoints.append(newPoint)
    return realPoints