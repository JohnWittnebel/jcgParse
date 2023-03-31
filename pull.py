## -*- coding: utf-8 -*-

import requests
import sys
import json
import codecs
import datetime
from patchDates import *

# Returns the patch that was active at the time of the input date
def getPatch(date):
    mostRecent = dates[0][1]
    for day in dates:
        if (day[0] < date):
            mostRecent = day[1]
    return mostRecent

# Does most of the actual work of getRecent, and should only be called by that function.
def getRecentFromLink(link):
    r = requests.get(link)
    with codecs.open("tempjcg.txt", "w", encoding='utf-8') as out:
        out.write(r.text)
    htmlfile = open("tempjcg.txt", 'r')
    nextline = htmlfile.readline()

    top16Tours = []
    groupTours = []

    while (nextline.find("</html>") == -1):
        if (nextline.find("schedule-link") != -1):
            tourNum = nextline[95:107]
            while (nextline.find("schedule-date") == -1):
                nextline = htmlfile.readline()
            dateline = nextline
            year = dateline[67:71]
            month = dateline[72:74]
            day = dateline[75:77]
            tourdate = datetime.datetime(int(year), int(month), int(day))
            patch = getPatch(tourdate)
            htmlfile.readline()
            htmlfile.readline()
            nextline = htmlfile.readline()
            if (nextline.find("トーナメント") != -1):
              #  print(tourNum)
                top16Tours.append([tourNum, patch])
            else:
              #  print(tourNum)
                groupTours.append([tourNum, patch])
        nextline = htmlfile.readline()

    return [groupTours, top16Tours]


# Writes the entrylist from the jcg with the input tournament number to "entrylist.txt"
# Returns two lists; the first list are the tournaments starting with 256 entrants (sorted from newest to
# oldest), the second list are the corresponding matches from the top 16 of the corresponding
# tournaments
# Output is a pair of lists, group round and top 16 rounds, respectively. Each list has entries of
# the form ["tour number", "name of patch"]
def getRecent():
    # Pull the most recent rotation JCGs so that the user can determine the tour number without
    # going to the JCG website
    # Page2 are the older tournament results
    # This could probably be made into a single page pull
    page2 = getRecentFromLink('https://sv.j-cg.com/past-schedule/rotation?page=2')
    page1 = getRecentFromLink('https://sv.j-cg.com/past-schedule/rotation')

    ret = page1

    for tour in page2[0]:
        ret[0].append(tour)

    for tour in page2[1]:
        ret[1].append(tour)

    return ret


# Writes the entrylist from the jcg with the input tournament number to "entrylist.txt"
# Writes the json of the tournament page with the input tournament number to "data.txt"
def jcgPull(tourNum):
    # We take in the tournament id that we want to analyze as input, later on this should be part of the UI
    r = requests.get("https://sv.j-cg.com/competition/" + tourNum + "/entries")
    with codecs.open("temp.txt", "w", encoding='utf-8') as out:
        out.write(r.text)
    datafile = open("temp.txt", 'r')
    nextline = datafile.readline()
    while ((nextline.find("list:") == -1) and (nextline.find("</html>") == -1)):
        nextline = datafile.readline()
    f = open("entrylist.txt", "w")
    f.write("{\"data\":")
    f.write(nextline[14:len(nextline) - 2])
    f.write("}")
    f.close()

    # There isnt a json file corresponding to this, codecs is used to deal with non-ascii characters
    r = requests.get("https://sv.j-cg.com/competition/" + tourNum + "/bracket")
    with codecs.open("temp2.txt", "w", encoding='utf-8') as out:
        out.write(r.text)
    bracketfile = open("temp2.txt", 'r')
    nextline = bracketfile.readline()
    while ((nextline.find("INLINE") == -1) and (nextline.find("</html>") == -1)):
        nextline = bracketfile.readline()
    f = open("data.txt", "w")
    f.write(nextline[31:])
    f.close()

#jcgPull(sys.argv[1])
#print(getRecent())
