import datetime

class Person:

    def __init__(self, number, name, nickname):
        self.number = number
        self.name = name
        self.nickname = nickname
        self.circles = {}
        self.plus1s = 0
        self.comments = 0
        self.firstInteraction = datetime.datetime(datetime.MAXYEAR, 12, 30, 0, 0, 0, 0, datetime.timezone.utc)
        self.lastInteraction = datetime.datetime(datetime.MINYEAR, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

    def __repr__(self):
        return "[Number: " + self.number + ", Name: " + self.name + ", Nicknames: " + self.nickname + ", Interactions: " + str(self.plus1s + self.comments) + "]"

    def addCircle(self, circle):
        self.circles.update({circle.name : circle})

    def updateFirstInteraction (self, time):
        if time < self.firstInteraction:
            self.firstInteraction = time

    def getLastInteraction(self):
        return self.lastInteraction

    def getFirstInteraction(self):
        return self.lastInteraction

    def updateLastInteraction (self, time):
        if time > self.lastInteraction:
            self.lastInteraction = time

    def updatePlus1s(self):
        self.plus1s+=1

    def updateComments(self):
        self.comments+=1

    def totalInteractions(self):
        return self.plus1s + self.comments

    def getPlus1s(self):
        return self.plus1s

    def getComments(self):
        return self.comments
