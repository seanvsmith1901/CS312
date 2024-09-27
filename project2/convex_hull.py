# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point

import Point
import Hull
import random

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:

    pointsButAsActualPoints = makePoints(points) # turns our list of points into a point object with a head and whatnot
    new_hull = Hull(pointsButAsActualPoints)
    new_hull = create_hull(new_hull)
    new_list = new_hull.create_list()
    return new_list


def create_hull(hull):

    our_median = median(hull)
    leftList = []
    rightList = []

    for point in points:
        if point[0] > our_median[0]:
            leftList.append(point)
        else:
            rightList.append(point)

    if len(leftList) > 3:
        newHull = Hull(leftList)
        create_hull(newHull)

    if len(rightList) > 3:
        newHull = Hull(leftList)
        create_hull(newHull)

    left_hull = formalizeHull(left_list)
    right_hull = formalizeHull(right_list)

    return joinHull(left_hull, right_hull)





    return []


def joinHull(leftHull, rightHull):
    temp1 = find_upper_tangent(leftHull, rightHull)
    temp2 = find_lower_tangent(leftHull, rightHull)
    # do da shimmy
    # create a new hull from these two and make a hull from that point adn all its pointers
    return temp1

def formalizeHull(listOfPoints):
    if len(listOfPoints) == 3:
        pass
    if len(listOfPoints) == 2:
        pass
    if len(listOfPoints) == 1:
        pass



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
        while slope(L.returnCC, R) > currSlopeL:
            L = L.returnCC
            currSlopeL = slope(L, R)
            done = 0
        while slope(L, R.returnCC) < currSlopeR:
            R = R.returnCL
            currSlopeR = slope(L,R)

    return temp # these are teh points that we need to link up


def find_lower_tangent(L,R):
    #leftHead = L
    #rightHead = R
    temp = (L,R)
    done = 0
    while not done:
        done = 1
        temp = (L,R)
        while slope(L.returnCl, R) < currSlopeL:
            L = L.returnCl
            currSlopeL = slope(L,R)
            done = 0
        while slope(L, R.returnCC) > currSlopeR:
            R = R.returnCC
            currSlopeR = slope(L,R)
            done = 0

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