import sys
import os
from bs4 import BeautifulSoup
from GPlusCircle import GPlusCircle
from Person import Person
class GPlusCalc:


    def main(self):
        takeout = sys.argv[1]
        #print (takeout)
        #saveLoc = sys.argv[2]
        print("sdfda")
        users = {}
        directory = os.fsencode(takeout + "/Google+ Circles")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".vcf"):
                circle = GPlusCircle(filename[0:len(filename)-4])
                print(circle.name)
                name = ""
                number = ""
                nickname = ""
                with open(takeout + "/Google+ Circles" + "/"  + filename) as vcf:
                    for line in vcf:
                        if line[0:3] == "FN:":
                            name = line[3:len(line)].rstrip()
                        elif line[0:3] == "URL":
                            number = line[29:len(line)].rstrip()
                        elif line[0:3] == "NIC":
                            nickname = line[9:len(line)].rstrip()
                        elif line[0:3] == "END":
                            person = Person(number, name, nickname)
                            person.addCircle(circle)
                            users.update({number : person})
                            circle.addPerson(person)
                            name = ""
                            number = ""
                            nickname = ""
                continue
            else:
                continue
        print(users)
        print(len(users))



if __name__ == '__main__':
    GPlusCalc().main()
