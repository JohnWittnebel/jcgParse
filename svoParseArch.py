## -*- coding: utf-8 -*-

from fractions import Fraction
import json
import sys
from archsMod import archs
from archsMod import association

############## GLOBAL FILES ############

datafile = open("data.txt", 'r')
entrylist = open("data.csv", 'r')

############## CONSTANTS ###############

general = 12
numClasses = 8
numArchs = len(archs)

########################################

def sortSecond(val):
    return val[1]

# Takes as input the full list of players
# Returns a list of players who actually participated in the tournament
def top256(dct):
    outputplayers = []
    for player in dct:
        if player["te"]:
            outputplayers.append(player)
    return outputplayers

def getarch(hashval):
    # Make sure that all the indicators are in the decklist we are looking at
    for i in range(numArchs):
        correct = 1
        for ind in archs[i][1]:
            if (hashval.find(ind) == -1):
                correct = 0
        if (correct == 1):
            if (i == numArchs - 1):
                print(hashval)
            return i
    # We should never get here
    print "ERROR: deck does not qualify as any archetype"
    return 1000

# Takes as input a list of participants
# Returns a table with the participants name and the archetypes they played, each entry in of the form:
# [playername, arch1, arch2, arch3]
def createTable():
    table = []
    entrylist.readline()
    for line in entrylist:
        player = []
        index1 = 0
        index2 = line.find(",")

        # The first section has the player names
        player.append(line[index1:index2])

        # The next 2 sections have the player ID#
        #for i in range(2):
        #    line = line[index2+1:]
        #    index2 = line.find(",")

        # The next 3 sections are the deck links
        for i in range(3):
            line = line[index2+1:]
            index2 = line.find(",")
            player.append(getarch(line[0:index2]))
        #print player
        table.append(player)

    return table

def archetype_selection(participants, arch):
    output = 0
    for player in participants:
        for deck in player['dk']:
            if (getarch(deck['hs']) == arch):
                output += 1
    return output

def get_archetype_selection(participants):
    output = []
    for i in range(len(archs)):
        num_of_i = archetype_selection(participants, i)
        output.append(num_of_i)
    return output

def print_arch_selection(participants):
    print "Number of Entrants for each archetype:"
    arch_distrib = get_archetype_selection(participants)
    for i in range(len(archs)):
        print archs[i][0] + ": " + str(arch_distrib[i])

# This should only ever be called by createMatchTable(), it requires the datafile to be at a specific
# point to extract the result of the "next" match
# Match entries are of the form [Player1, Player2, Winner (either 1 or 2)]
def getMatchEntry():
    #skipping html lines to get to actual info
    for i in range(8):
        datafile.readline()

    #next line has number of games won for the first player
    score1 = datafile.readline()[23]

    #the next line has the first player, hidden in html
    helper = datafile.readline()
    index1 = helper.find(">")
    index2 = helper.rfind("<")
    player1 = helper[index1+1:index2]

    #skipping more html lines to get to info
    datafile.readline()
    helper = datafile.readline()
    isWinnerTwo = helper.find("winner")

    #Same as for score1 and player1
    score2 = datafile.readline()[23]
    helper = datafile.readline()
    index1 = helper.find(">")
    index2 = helper.rfind("<")
    player2 = helper[index1+1:index2]

    #making non-english characters work with playerTable
    player1 = player1.decode('utf-8')
    player2 = player2.decode('utf-8')

    if (isWinnerTwo < 0):
        return [player1, player2, 1]
    else:
        return [player1, player2, 2]

# Returns a table of all the matches in data.txt by going through the html (this doesnt currently include top 16).
def createMatchTable():
    matchTable = []
    nextline = datafile.readline()

    #simple hack, the end of the file will close the html
    while (nextline.find("</html>") == -1):
        #whenever we see a match, this may have to be changed, it is a little sensitive
        if (nextline.find("onClick=") > -1):
            matchTable.append(getMatchEntry())
        nextline = datafile.readline()

    return matchTable

# Cross-references playerTable and matchTable to determine the number of wins and losses for each
# archetype.
# Mutates archSetWins, archSetLosses, and playerTable. matchTable is kept constant
def crossReference(playerTable, matchTable, archSetWins, archSetLosses):
    for match in matchTable:
        # Get winner/loser from the current match
        winner = match[2]-1
        loser = match[2] % 2

        for player in playerTable:
            if ((match[winner] == player[0]) and (player[3] != 4) and (player[4] != 1)):
                player[3] += 1
                archSetWins[player[1]] += 1
                archSetWins[player[2]] += 1
            if ((match[loser] == player[0]) and (player[3] != 4) and (player[4] != 1)):
                player[4] += 1
                archSetLosses[player[1]] += 1
                archSetLosses[player[2]] += 1


def obtainArch(playerName, playerClass, playerEntry):
    for entry in association:
        if (entry[0] == playerClass):
            for arch in entry[1]:
                for playerArch in playerEntry:
                    if (playerArch == arch):
                        return arch
    return general


# Cross-references the playerTable and the matchTable in order to fill out the matchupMatrix.
# matchupMatrix is mutated. playerTable and matchTable are kept constant
def fillMatchupMatrix(matchupMatrix, playerTable, data):
    for match in data:
        if (match['isBye']):
            continue

        player1 = match['top']['team']['name']
        player2 = match['bottom']['team']['name']

        for i in range(len(playerTable)):
            if (playerTable[i][0].decode('utf-8') == player1):
                player1index = i
            if (playerTable[i][0].decode('utf-8') == player2):
                player2index = i

        if 'stats' in match:
            for game in match['stats']:
                if (game['stats']['top']['winner']):
                    winner = 1
                else:
                    winner = 2

                player1class = game['stats']['top']['class']
                player2class = game['stats']['bottom']['class']

                player1arch = obtainArch(player1, player1class, playerTable[player1index])
                player2arch = obtainArch(player2, player2class, playerTable[player2index])

                if (winner == 1):
                    if (player1arch == 14) and (player2arch == 12):
                        print playerTable[player1index]
                        print player1class
                    matchupMatrix[player1arch][player2arch][0] += 1
                    matchupMatrix[player1arch][player2arch][1] += 1
                    matchupMatrix[player2arch][player1arch][1] += 1
                else:
                    if (player2arch == 14) and (player1arch == 12):
                        print playerTable[player2index]
                        print player2class
                        print "2"
                    matchupMatrix[player2arch][player1arch][0] += 1
                    matchupMatrix[player2arch][player1arch][1] += 1
                    matchupMatrix[player1arch][player2arch][1] += 1

    #for match in matchTable:
    #    winner = -1
     #   loser = -1
     #   if (match[2] == 2):
     #       winner = 1
     #       loser = 0
     #   else:
     #       winner = 0
     #       loser = 1

     #   winClass1 = -1
     #   winClass2 = -1
     #   lossClass1 = -1
     #   lossClass2 = -1

     #   for player in playerTable:
     #       if (match[winner] == player[0]):
     #           winClass1 = player[1]
     #           winClass2 = player[2]
     #       if (match[loser] == player[0]):
     #           lossClass1 = player[1]
     #           lossClass2 = player[2]

     #   if ((winClass1 == -1) or (winClass2 == -1) or (lossClass1 == -1) or (lossClass2 == -1)):
            #something weird happened, the player decks werent found in the JSON
     #       continue

     #   if (not (((winClass1 == lossClass1) and (winClass2 == lossClass2))
     #       or ((winClass1 == lossClass2) and (winClass2 == lossClass1)))):
     #       matchupMatrix[winClass1][lossClass1][0] += 1
     #       matchupMatrix[winClass2][lossClass1][0] += 1
     #       matchupMatrix[winClass1][lossClass1][1] += 1
     #       matchupMatrix[winClass2][lossClass1][1] += 1

     #       matchupMatrix[winClass1][lossClass2][0] += 1
     #       matchupMatrix[winClass2][lossClass2][0] += 1
     #       matchupMatrix[winClass1][lossClass2][1] += 1
     #       matchupMatrix[winClass2][lossClass2][1] += 1

     #       matchupMatrix[lossClass1][winClass1][1] += 1
     #       matchupMatrix[lossClass1][winClass2][1] += 1
     #       matchupMatrix[lossClass2][winClass1][1] += 1
     #       matchupMatrix[lossClass2][winClass2][1] += 1

# Output links to all the decks used, along with how many wins they got while in the top 16.
def printAllDecks(participants, playerTable):
    wins = 4
    while (wins > -1):
        top16out.write("Wins: " + str(wins) + "\r\n")
        for player in participants:
            for playr in playerTable:
                if (player['nm'] == playr[0]):
                    if (playr[3] == wins):
                        for deck in player['dk']:
                            top16out.write(archs[getarch(deck['hs'])][0] + "\r\n")
                            top16out.write("https://shadowverse-portal.com/deck/" + deck['hs'] + "\r\n")
        top16out.write("\r\n")
        wins -= 1

def main():
    # Initiating lists that will be used
    archSetWins = []
    archSetLosses = []
    winrateTable = []
    matchupMatrix = []

    for i in range(numArchs):
        archSetWins.append(0)
        archSetLosses.append(0)
        winrateTable.append([archs[i][0], 0])
        nextrow = []
        for j in range(numArchs):
            nextrow.append([0,0])
        matchupMatrix.append(nextrow)

    # Get the json that was pulled
    jsonfile = open("data.txt", 'r')
    data = json.loads(jsonfile.readline())
    jsonfile.close()

    # Make the table of players, entries are of the form: [Name, Arch1, Arch2, Arch3]
    playerTable = createTable()

    # Uses the playerTable and data in order to fill out the matchup matrix.
    fillMatchupMatrix(matchupMatrix, playerTable, data)

    for i in range(numArchs):
        wins = 0
        losses = 0
        for j in range(numArchs):
            wins += matchupMatrix[i][j][0]
            losses += (matchupMatrix[i][j][1] - matchupMatrix[i][j][0])
        if (wins + losses == 0):
            winrateTable[i][1] = 0
        else:
            winrateTable[i][1] = Fraction(wins, wins + losses)

    winrateTable.sort(key = sortSecond)

    print "\nWinrates:"
    for i in range(numArchs):
        print (winrateTable[i][0] + " = " + str(round(float(winrateTable[i][1]),4)))

  #  print "\nSets won by each archetype: "
  #  print archSetWins
   # print "\nSets lost by each archetype: "
 #   print archSetLosses
  #  print "\nNumber of each archetype hitting top 16: "
   # print top16
    print "\nMatchup Matrix:"
    for i in range(numArchs):
   #     matrixfile.write(str(matchupMatrix[i]) + "\n")
        print archs[i][0] + ": " + str(matchupMatrix[i])


main()
