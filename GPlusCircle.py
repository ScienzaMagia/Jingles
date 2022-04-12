


class GPlusCircle:

    def __init__(self, name):
        self.members = {}
        self.name = name


    def addPerson(self, person):
        self.members.update({person.number : person})
