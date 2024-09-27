# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point

import Point
import random

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:

    pointsButAsActualPoints = makePoints(points) # turns our list of points into a point object with a head and whatnot

    leftList = []
    rightList = []
    side = "L"





    #head = Point # thats not gonna work lol
    our_median = median(points)
    print(our_median) # so this should? find the median in terms of its x position
    for point in points:
        if point[0] > our_median[0]:
            leftList.append(point)
        else:
            rightList.append(point)

    if len(list) == 1:
        new_point = Point(list[0][0], list[0][1], list[0], list[0])

    elif len(list) == 2:
        if side == "L":
            pass
            # find rightmost point
            # make that the head
        else:
            pass
            # find leftmost point
            # make that the head

    elif len(list) == 3:
        pass # theres a whole LIST of things that need to happen here lol



    return []


def median(S): # s is teh list,



    # just copying the pseducode given on the slides
    return selection(S, len(S)/2)


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


def selection(S, k):
    Sl = []
    Sr = []
    Sv = []
    # need a random pivot v. there are better ways to pick it. I am not going to do that.
    v = S[(random.randint(0, len(S)-1))][0]


    # choose a random pivot
    for i in range(len(S)):
        if S[i][0] < v:
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