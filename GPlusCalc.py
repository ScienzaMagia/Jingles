import sys
import os
import csv
import re
import datetime
from bs4 import BeautifulSoup
from GPlusCircle import GPlusCircle
from Person import Person


class GPlusCalc:


    def main(self):
        takeout = sys.argv[1]

        ## Extracts users from saved circle data ##
        self.unknownCount = 0
        self.users = {}
        self.userAvatars = {}
        self.circles = {"Not Followed":GPlusCircle("Not Followed")}



        print("Extracting Users")
        self.extractUsers(takeout, "+1s on posts.html", "THUMBS-CORRESPOND")
        self.extractUsers(takeout, "Comments.html", "THUMBS-CORRESPOND")
        self.extractUsers(takeout, "+1s on comments.html", "THUMBS-DONT-CORRESPOND")

        print ("Processing Circles")
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
                            url = re.sub(r'\\', "", line[4:len(line)].rstrip())
                        elif line[0:3] == "NIC":
                            nickname = line[9:len(line)].rstrip()
                        elif line[0:3] == "END":
                            if name in self.users:
                                self.users[name].url = url
                                self.users[name].nickname = nickname
                                self.users[name].addCircle(circle)
                                circle.addPerson(self.users[name])
                            else:
                                person = Person(url, name, nickname, "")
                                self.users.update({name : person})
                                circle.addPerson(person)
                            name = ""
                            number = ""
                            nickname = ""
                continue
            else:
                continue


        ## Like Processing from file ##
        print ("Processing +1s on posts")
        self.extractInteractions(takeout, "+1s on posts.html")
        print ("Processing comments on posts")
        self.extractInteractions(takeout, "Comments.html")
        print ("Processing +1s on comments")
        self.extractInteractions(takeout, "+1s on comments.html")




        #Writing contents to csv
        print("Writing data to .CSV")
        f = open('Users.csv', 'w')
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Profile URL","Name", "Nickname", "Avatar", "+1s", "Comments", "Total", "First Interaction", "Last Interaction"])
        for u in self.users:
            csvwriter.writerow([self.users[u].url, self.users[u].name, self.users[u].nickname, self.users[u].avatar, self.users[u].getPlus1s(), self.users[u].getComments(), self.users[u].totalInteractions(), self.users[u].getFirstInteraction(), self.users[u].getLastInteraction()])
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


    def extractUsers(self, takeout, filename, mode):
            if os.path.exists(takeout + "/Google+ Stream/ActivityLog/" + filename):
                with open(takeout + "/Google+ Stream/ActivityLog/" + filename, 'r') as f:
                    contents = f.read()
                    interactionSoup = BeautifulSoup(contents, "html.parser")
                    items = interactionSoup.find_all(class_ = "item")
                    for i in items:
                        currentAvatar = i.a.img["src"]
                        if (currentAvatar in self.userAvatars) == False:
                            currentname = ""
                            if mode == "THUMBS-CORRESPOND": #Runs when the name attached to activity stream is the same as the user being interacted with
                                currentName = str(i.div.a.string)
                                offset = currentName.find("by ")
                                if offset == -1:
                                    currentName = "Unknown-" + str(self.unknownCount)
                                    self.unknownCount+=1
                                else:
                                    currentName = self.nameCleanup(currentName[(offset+3):len(i.div.a.string)].rstrip())
                            else:
                                currentName = "Unknown-" + str(self.unknownCount)
                                self.unknownCount+=1
                            self.userAvatars.update({currentAvatar : currentName})
                            newGuy = Person("", currentName, "", currentAvatar)
                            self.users.update({currentName:newGuy})






    def extractInteractions(self, takeout, filename,):
            if os.path.exists(takeout + "/Google+ Stream/ActivityLog/" + filename):
                with open(takeout + "/Google+ Stream/ActivityLog/" + filename, 'r') as f:
                    contents = f.read()
                    interactionSoup = BeautifulSoup(contents, "html.parser")
                    items = interactionSoup.find_all(class_ = "item")
                    for i in items:
                        currentAvatar = str(i.a.img["src"])
                        currentTime = datetime.datetime.strptime(i.div.div.span["title"], "%Y-%m-%dT%H:%M%z")
                        if (filename.find("+1") != -1):
                            self.users[self.userAvatars[currentAvatar]].updatePlus1s()
                        else:
                            self.users[self.userAvatars[currentAvatar]].updateComments()
                        self.users[self.userAvatars[currentAvatar]].updateFirstInteraction(currentTime)
                        self.users[self.userAvatars[currentAvatar]].updateLastInteraction(currentTime)










if __name__ == '__main__':
    GPlusCalc().main()
