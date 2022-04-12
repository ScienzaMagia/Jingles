import sys
import os
import datetime
from bs4 import BeautifulSoup
from GPlusCircle import GPlusCircle
from Person import Person
class GPlusCalc:


    def main(self):
        takeout = sys.argv[1]


        ## Extracts users from saved circle data ##

        users = {}
        circles = {}
        directory = os.fsencode(takeout + "/Google+ Circles")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".vcf"):
                circle = GPlusCircle(filename[0:len(filename)-4])
                circles.update({filename[0:len(filename)-4] : circle})
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
                            users.update({name : person})
                            circle.addPerson(person)
                            name = ""
                            number = ""
                            nickname = ""
                continue
            else:
                continue
        #print (circles)


        ## Like Processing from file ##

        if os.path.exists(takeout + "/Google+ Stream/ActivityLog/+1s on posts.html"):
            with open(takeout + "/Google+ Stream/ActivityLog/+1s on posts.html", 'r') as f:
                contents = f.read()
                commentHtml = BeautifulSoup(contents, "html.parser")
                interactions = commentHtml.find_all(class_ = "text")
                currentName = ""
                for i in interactions:
                    #print (i.a.string)
                    currentName = i.a.string[13:len(i.a.string)]
                    currentTime = i.div.span["title"]
                    #print(currentTime)
                    #print(currentName)
                    if currentName in users:
                        users.get(currentName).updatePlus1s()
                        #print(currentName + ", " + str(users.get(currentName).getPlus1s()))
                    #print (i.string)

                    #"2018-05-17T15:45+0000">


                #doc = open("pretty.html", "w")
                #doc.writelines(interactions)
                #doc.close()


        #

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

if __name__ == '__main__':
    GPlusCalc().main()
