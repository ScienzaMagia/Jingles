import sys
import os
from bs4 import BeautifulSoup

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
                print(filename)
                doc = open(takeout + "/Google+ Circles" + filename + ".vcf", "r")

                # print(os.path.join(directory, filename))
                continue
            else:
                continue




if __name__ == '__main__':
    GPlusCalc().main()
