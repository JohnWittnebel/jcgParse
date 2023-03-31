from pull import *
from parseArch import *
from combine import *
from patchDates import *
import os

mostRecent = getRecent()

tourFile = open("tempjcg.txt","r")

fullResults = 0

print "Would you like the full results from a specific patch? (y/n)"
uinput = raw_input("")

if (uinput == "n"):

    print "Which JCG would you like the results from?"
    for i in range(len(mostRecent[0])):
        print str(i+1) + ": " + str(mostRecent[0][i][0]) + ": " + mostRecent[0][i][1]
    uinput = int(raw_input(""))

    jcgPull(mostRecent[0][uinput-1][0])
    main()
elif (uinput == "y"):
    exp = mostRecent[0][0][1]
    i = 0
    while (mostRecent[0][i][1] == exp):
        for j in range(2):
            print mostRecent[j][i][0]
            jcgPull(mostRecent[j][i][0])
            main()
            os.remove("data.txt")
            os.remove("entrylist.txt")
        i += 1
    initCombMat(comMatrix)
    comMatrix = collapseRows(comMatrix, -1)
    printInfo(comMatrix)
elif (uinput == "b"):
    print(mostRecent[0][0][1]) 
    for j in range(2):
        print mostRecent[j][0][0]
        jcgPull(mostRecent[j][0][0])
        main()
        os.remove("data.txt")
        os.remove("entrylist.txt")
    initCombMat(comMatrix)
    comMatrix = collapseRows(comMatrix, -1)
    printInfo(comMatrix)
elif (uinput == "a"):
    print(mostRecent[0][0][0])
    #jcgPull(mostRecent[0][0][0])
    jcgPull("k3HeLraSI0ds")
    main()
else:
    print "y/n only"


#if combining
#initCombMat(comMatrix)
#comMatrix = collapseRows(comMatrix)
#printInfo(comMatrix)
