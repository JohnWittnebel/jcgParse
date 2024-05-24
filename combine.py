import ast
from archsMod import archs
from fractions import Fraction

numArchs = len(archs)
comMatrix = []

def sortSecond(val):
    return val[1]

# combines two rows of tuple with the same length
def combineRows(row1,row2):
    if (len(row1) != len(row2)):
        print "ERROR: Attempted to combine rows of different length"
        return -1
    for j in range(len(row1)):
        row1[j][0] += row2[j][0]
        row1[j][1] += row2[j][1]
    return row1

def printMatrix(imat):
    for i in range(len(imat)):
        print imat[i]

def initCombMat(imat):
    for i in range(len(archs)):
        comMatrix.append(0)

def collapseRows(iMatrix, ban):
    i=0
    matrixfile = open("archmatrix.txt", "r")
    f1 = matrixfile.readlines()
    for x in f1:
        if (iMatrix[i] == 0):
            if (ban == -1):
              iMatrix[i] = ast.literal_eval(x)
            else:
              iMatrix[i] = (ast.literal_eval(x))[0:ban] + (ast.literal_eval(x))[ban+1:]
        else:
            if (ban == -1):
              iMatrix[i] = combineRows(iMatrix[i], ast.literal_eval(x))
            else:
              iMatrix[i] = combineRows(iMatrix[i], (ast.literal_eval(x))[0:ban] + (ast.literal_eval(x))[ban+1:])
        if (i == len(archs)-1):
            i = 0
        else:
            i += 1
    return iMatrix

#TODO: this is similar to what is done in parseArch, generalize+combine
def printInfo(iMatrix):
    winrates = []
    for i in range(numArchs):
        print str(archs[i][0]) + ": " + str(iMatrix[i])
        winrates.append([archs[i][0],0])
    for i in range(numArchs):
        classWins = 0
        classGames = 0
        for j in range(numArchs):
            classWins += iMatrix[i][j][0]
            classGames += iMatrix[i][j][1]
        print archs[i][0] + ": " + str(classGames/2) + " - " + str(classWins/2) + " - " + str((classGames-classWins)/2)
        winrates[i][1] = Fraction(classWins,classGames)
    ###
    winrates.sort(key = sortSecond)
    for i in range(len(winrates)):
        print (winrates[i][0] + " = " + str(round(float(winrates[i][1]),4)))
    ###
    #return winrates
    ###

def printWinrateGivenBan(iMatrix, baseWinrates):
  winrates = []
  for i in range(numArchs):
    print str(archs[i][0]) + ": " + str(iMatrix[i])
    winrates.append([archs[i][0],0])
  for i in range(numArchs):
    classWins = 0
    classGames = 0
    for j in range(numArchs - 1):
      classWins += iMatrix[i][j][0]
      classGames += iMatrix[i][j][1]
    print archs[i][0] + ": " + str(classGames/2) + " - " + str(classWins/2) + " - " + str((classGames-classWins)/2)
    winrates[i][1] = Fraction(classWins,classGames) #- round(float(baseWinrates[i][1]),4) ##
  winrates.sort(key = sortSecond)
  for i in range(len(winrates)):
    print (winrates[i][0] + " = " + str(round(float(winrates[i][1]),4)))

def banWrapper():
  global comMatrix
  comMatrix = collapseRows(comMatrix, -1)
  baseWinrates = printInfo(comMatrix)
  resetCombMat()
  for i in range(numArchs):
      print "Winrates Given that " + archs[i][0] + " is banned:\n\n"
      #initCombMat(comMatrix)
      comMatrix = collapseRows(comMatrix, i)
      #comMatrix = collapseRows(comMatrix, i)
      printWinrateGivenBan(comMatrix, baseWinrates)
      resetCombMat()
      print "\n"

def resetCombMat():
  for i in range(numArchs):
    comMatrix[i] = 0

def vsAllLineups(iMatrix, deck1, deck2, deck3):
  for i in range(numArchs):
      for j in range(numArchs - i - 1):
         matchup(iMatrix, deck1, deck2, deck3, i, i+j)

def matchup(iMatrix, A, B):
  thisMatchup = [[],[],[]]
  thisMatchup[0].append(iMatrix[A[0]][B[0]])
  thisMatchup[0].append(iMatrix[A[0]][B[1]])
  thisMatchup[1].append(iMatrix[A[1]][B[0]])
  thisMatchup[1].append(iMatrix[A[1]][B[1]])
  thisMatchup[2].append(iMatrix[A[2]][B[0]])
  thisMatchup[2].append(iMatrix[A[2]][B[1]])
  print("vs " + archs[B[0]][0] + " and " + archs[B[1]][0])
  print(thisMatchup)
  print("\n")

  winrates = []
  for i in range(3):
    print str(archs[A[i]][0]) + ": " + str(iMatrix[A[i]])
    winrates.append([archs[A[i]][0],0])
  for i in range(3):
    classWins = 0
    classGames = 0
    for j in range(2):
      classWins += thisMatchup[i][j][0]
      classGames += thisMatchup[i][j][1]
    print archs[A[i]][0] + ": " + str(classGames) + " - " + str(classWins) + " - " + str((classGames-classWins))
    winrates[i][1] = Fraction(classWins,classGames)
  winrates.sort(key = sortSecond)
  for i in range(len(winrates)):
    print (winrates[i][0] + " = " + str(round(float(winrates[i][1]),4)))

#initCombMat(comMatrix)
#comMatrix = collapseRows(comMatrix, -1)
#printInfo(comMatrix)
#matchup(comMatrix,[10,12,7],[2,0])

#initCombMat(comMatrix)
#banWrapper()


#comMatrix = collapseRows(comMatrix, -1)
#winrateGivenBan(comMatrix, 2)
#printInfo(comMatrix)
#winrateGivenBan(2)
