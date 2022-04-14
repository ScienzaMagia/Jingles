import sys
import os
import csv
import re
import itertools
import datetime
from bs4 import BeautifulSoup
from GCircle import GCircle
from Person import Person


class JinglesProcessor:


    def main(self):        
        directory = sys.argv[1]
        streamDir = os.path.join(directory, "Google+ Stream")
        logDir = os.path.join(streamDir, "ActivityLog")


        ## Extracts users from activity stream ##
        self.unknownCount = 0
        self.users = {}
        self.userAvatars = {}
        self.circles = {"Not Followed":GCircle("Not Followed")}

        print("Extracting Users from +1s")
        self.extractUsers(logDir, "+1s on posts.html", "THUMBS-CORRESPOND")
        print("Extracting Users from comments")
        self.extractUsers(logDir, "Comments.html", "THUMBS-CORRESPOND")
        print("Extracting Users from +1s on comments")
        self.extractUsers(logDir, "+1s on comments.html", "THUMBS-DONT-CORRESPOND")



        ## Extracts users from saved circle data ##
        print ("Processing Circles")
        circleDirectory = os.path.join(directory, "Google+ Circles")
        for file in os.listdir(circleDirectory):
            filename = os.fsdecode(file)
            if filename.endswith(".vcf"):
                circle = GCircle(filename[0:len(filename)-4])
                self.circles.update({filename[0:len(filename)-4] : circle})
                name = ""
                number = ""
                nickname = ""
                with open(os.path.join(circleDirectory, filename), 'r', encoding='utf-8') as vcf:
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


        ## Interaction processing from file ##
        print ("Processing +1s on posts")
        self.extractInteractions(logDir, "+1s on posts.html")
        print ("Processing comments on posts")
        self.extractInteractions(logDir, "Comments.html")
        print ("Processing +1s on comments")
        self.extractInteractions(logDir, "+1s on comments.html")




        ## Writing contents to csv ##

        print("Writing data to .CSV")
        f = open('Users.csv', 'w', newline='', encoding='utf-8')
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Profile URL","Name", "Nickname", "Avatar", "+1s", "Comments", "Total", "First Interaction", "Last Interaction"])
        for u in self.users:
            csvwriter.writerow([self.users[u].url, self.users[u].name, self.users[u].nickname, self.users[u].avatar, self.users[u].getPlus1s(), self.users[u].getComments(), self.users[u].totalInteractions(), self.users[u].getFirstInteraction(), self.users[u].getLastInteraction()])
        f.close()


        circleSet = []
        for c in self.circles:
            circleSet.append(self.circles[c].returnUsernames())



      
        columns = list(itertools.zip_longest(*circleSet, ""))
        f = open('Circles.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(self.circles.keys())
        
        writer.writerows(columns)
        #print(circleSet)
        #print("^circleSet vcolumns")
        #print(columns)
        f.close()


       
        #s    circleSet.update(self.circles[c].returnUsernames())

        


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
        


    def extractUsers(self, directory, filename, mode):
            if os.path.exists(os.path.join(directory, filename)):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                    contents = f.read()
                    interactionSoup = BeautifulSoup(contents, "html.parser")
                    items = interactionSoup.find_all(class_ = "item")
                    #printcounter = 1
                    for i in items:

                        # print("Processing: " + str(printcounter) + "/" + str(len(items)), end = "\r")
                        #printcounter += 1
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






    def extractInteractions(self, directory, filename,):
            if os.path.exists(os.path.join(directory, filename)):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
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
    JinglesProcessor().main()
