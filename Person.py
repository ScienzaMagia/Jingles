


class Person:

    def __init__(self, number, name, nickname):
        self.number = number
        self.name = name
        self.nickname = nickname
        self.circles = {}

    def __repr__(self):
        return "[" + self.number + ", " + self.name + ", " + self.nickname + "]"

    def addCircle(self, circle):
        self.circles.update({circle.name : circle})
