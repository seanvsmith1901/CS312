
class Point:

    __x = None
    __y = None
    __cl = None
    __cc = None


    def __init__(self, cc, cl, x,y):
        self.__x = x
        self.__y = y
        self.__cl = cl
        self.__cc = cc
        self.__checked = False

    def returnX(self):
        return self.__x

    def returnY(self):
        return self.__y

    def returnCL(self):
        return self.__cl

    def returnCC(self):
        return self.__cc

    def setCC(self, new_point):
        self.__cc = new_point

    def setCL(self, new_point):
        self.__cl = new_point

    def returnPoint(self):
        return [self.returnX(), self.returnY()]

    def check(self):
        self.__checked = True

    def unCheck(self):
        self.__checked = False

