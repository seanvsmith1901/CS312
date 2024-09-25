
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

    def returnCC(self):
        return self.__cc

    def returnX(self):
        return self.__x

    def returnY(self):
        return self.__y

    def returnCL(self):

        
        return self.__cl

    def returnPoint(self):
        return [self.returnX(), self.returnY()]

