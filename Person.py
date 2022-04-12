


class Person:

    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.circles = {}

    def __repr__(self):
        return "[" + self.number + ", " + self.name + "]"
        
    def addCircle(self, circle):
        self.circles.update({circle.name : circle})
