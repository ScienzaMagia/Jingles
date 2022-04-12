


class Person:

    def __init__(self, number, name, circles):
        self.number = number
        self.name = name
        self.circles = {}

    def addCircle(self, circle):
        self.circles.update(circle.name:circle)
