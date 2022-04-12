import sys
import os
import csv
import datetime
from bs4 import BeautifulSoup
from GPlusCircle import GPlusCircle
from Person import Person


class GPlusCalc:


    def main(self):
        takeout = sys.argv[1]

        ## Extracts users from saved circle data ##

        self.users = {}
        self.circles = {"Not Followed":GPlusCircle("Not Followed")}
        directory = os.fsencode(takeout + "/Google+ Circles")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".vcf"):
                circle = GPlusCircle(filename[0:len(filename)-4])
                self.circles.update({filename[0:len(filename)-4] : circle})
                name = ""
                number = ""
                nickname = ""
                with open(takeout + "/Google+ Circles" + "/"  + filename) as vcf:
                    for line in vcf:
                        if line[0:3] == "FN:":
                            name = self.nameCleanup(line[3:len(line)].rstrip())
                        elif line[0:3] == "URL":
                            number = line[29:len(line)].rstrip()
                        elif line[0:3] == "NIC":
                            nickname = line[9:len(line)].rstrip()
                        elif line[0:3] == "END":
                            person = Person(number, name, nickname)
                            person.addCircle(circle)
                            self.users.update({name : person})
                            circle.addPerson(person)
                            name = ""
                            number = ""
                            nickname = ""
                continue
            else:
                continue
        #print (circles)


        ## Like Processing from file ##
        print ("Processing +1s on posts")
        self.interactionExtractor(takeout, "+1s on posts.html")
        print ("Processing +1s on comments")
        self.interactionExtractor(takeout, "+1s on comments.html")
        print ("Processing comments on posts")
        self.interactionExtractor(takeout, "Comments.html")


        #Writing contents to csv
        print("Writing data to .CSV")
        f = open('Users.csv', 'w')
        csvwriter = csv.writer(f)
        csvwriter.writerow(["User Number","Name", "Nickname","+1s", "Comments", "Total", "First Interaction", "Last Interaction"])
        for u in self.users:
            csvwriter.writerow([self.users[u].number, self.users[u].name,self.users[u].nickname, self.users[u].getPlus1s(), self.users[u].getComments(), self.users[u].totalInteractions(), self.users[u].getFirstInteraction(), self.users[u].getLastInteraction()])
        f.close()

    def nameCleanup(self, name):

        communityFilter = name.find(" in ")
        if communityFilter != -1:
            name = name[0 : communityFilter]
        nickFilter = name.find("(")

        if nickFilter != -1:
            name = name[0 : nickFilter]

        quoteFilter = name.find("“")
        endQuoteFilter = name.find("”")
        if quoteFilter != -1 and endQuoteFilter != -1:
            name = name[0 : quoteFilter] + name[endQuoteFilter+2:len(name)]

        return name

    def interactionExtractor(self, takeout, filename):
            if os.path.exists(takeout + "/Google+ Stream/ActivityLog/" + filename):
                with open(takeout + "/Google+ Stream/ActivityLog/" + filename, 'r') as f:
                    contents = f.read()
                    interactionSoup = BeautifulSoup(contents, "html.parser")
                    interactions = interactionSoup.find_all(class_ = "text")
                    currentName = ""
                    for i in interactions:
                        currentName = str(i.a.string)
                        #                                               2012-12-25T17:25+0000
                        currentTime = datetime.datetime.strptime(i.div.span["title"], "%Y-%m-%dT%H:%M%z")
                        offset = currentName.find("by ")

                        if offset == -1:
                            currentName = "[Unknown Name]"
                        else:
                            currentName = self.nameCleanup(currentName[(offset+3):len(i.a.string)])
                        if currentName in self.users:
                            if (filename.find("+1") != -1):
                                self.users.get(currentName).updatePlus1s()
                            else:
                                self.users.get(currentName).updateComments()
                            self.users.get(currentName).updateFirstInteraction(currentTime)
                            self.users.get(currentName).updateLastInteraction(currentTime)
                        else:
                            newGuy = Person("Unknown", currentName, "Unknown")
                            self.circles["Not Followed"].addPerson(newGuy)
                            self.users.update({currentName:newGuy})


if __name__ == '__main__':
    GPlusCalc().main()
