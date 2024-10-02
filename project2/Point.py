
class Point:


    def __init__(self, x, y, cl, cc):
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


    def check(self):
        self.__checked = True

    def unCheck(self):
        self.__checked = False

    def returnChecked(self):
        return self.__checked

    def __getitem__(self, item):
        return item