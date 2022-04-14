


class GPlusCircle:

    def __init__(self, name):
        self.users = {}
        self.name = name


    def __repr__(self):
        return "[" + self.name + ", " + str(len(self.members)) + "]"

    def addPerson(self, person):
        self.users.update({person.name : person})

    def __len__(self):
        return len(self.members)

    def returnUsers(self):
        return self.users
    
    def returnUsernames(self):
        usernames = []
        for u in self.users:
            usernames.append(u)
        return usernames
