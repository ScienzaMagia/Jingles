


class GPlusCircle:

    def __init__(self, name):
        self.members = {}
        self.name = name


    def __repr__(self):
        return "[" + self.name + ", " + str(len(self.members)) + "]"

    def addPerson(self, person):
        self.members.update({person.name : person})

    def __len__(self):
        return len(self.members)
