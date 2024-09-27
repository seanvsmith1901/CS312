import Point

class Hull: # literally just list of points but I like having it as a class :)

    def __init__(self):
        self.hull = []

    def __add__(self, Point):
        self.hull.append(Point)