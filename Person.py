


class Person:

    def __init__(self, number, name, nickname):
        self.number = number
        self.name = name
        self.nickname = nickname
        self.circles = {}
        self.plus1s = 0
        self.comments = 0
        self.firstInteraction = ""
        self.lastInteraction = ""

    def __repr__(self):
        return "[" + self.number + ", " + self.name + ", " + self.nickname + "]"

    def addCircle(self, circle):
        self.circles.update({circle.name : circle})

    def updatePlus1s(self):
        self.plus1s+=1

    def updateComments(self):
        self.comments+=1

    def totalInteractions(self):
        return self.plus1s + comments

    def getPlus1s(self):
        return self.plus1s

    def getComments(self):
        return self.comments
