## -*- coding: utf-8 -*-

import requests
from fractions import Fraction
import json
import sys
import os
from archsMod import archs
from archsMod import lineups

############## GLOBAL FILES ############

############## CONSTANTS ###############

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
        if player['result']:
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
            #####
            # For finding specific archetypes
            #if (i == numArchs - 5):
            #    print hashval
            #
            #####
            return i
    # We should never get here
    print "ERROR: deck does not qualify as any archetype"
    return 1000

# Takes as input a list of participants
# Returns a table with the participants name and the archetypes they played, each entry in of the form:
# [playername, arch1, arch2, additional data]
def createTable(participants):
    table = []
    for player in participants:
        #if len(player['dk']) == 0:
            # This can occur if someone who didnt register their decks in time (but still gets in from waitlist) makes top 16
            # ignore this player for now, maybe try and fix it later, but it seems like a lot of
            # work
            # continue
        playerentry = [player['nicename']]
        for deck in player['sv_decks']:
            playerentry.append(getarch(deck['hash']))
        #########
        ######### FOR WHEN LOOKING AT 2D0B Lineup v Lineup:

        #########
        #########
        #playerDecksToLineup(playerentry)
        ######
        playerentry.append(0)
        playerentry.append(0)
        #if (playerentry[1] == 9) or (playerentry[2] == 9):
        #    print player['name']
        table.append(playerentry)
    return table

def playerDecksToLineup(playerentry):
    lineupindex = 0
    for lineup in lineups:
        if (lineup[0] == playerentry[0] and lineup[1] == playerentry[1]) or (lineup[1] == playerentry[0] and lineup[0] == playerentry[1]):
            playerentry[1] = lineupindex
            playerentry[2] = 0
            return
        else:
            lineupindex += 1
    playerentry[1] = -1
    playerentry[2] = 0

def archetype_selection(participants, arch):
    output = 0
    for player in participants:
        for deck in player['sv_decks']:
            if (getarch(deck['hash']) == arch):
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
def getMatchEntry(datafile):
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

# Does what createMatchTable did after JCG site rework
def newCreateMatchTable(datafile):
    matchTable = []

    jsonfile = open("data.txt", 'r')
    data = json.loads(jsonfile.readline())
    jsonfile.close()
    for group in data['groups']:

      currSec = requests.get("https://sv.j-cg.com/api/competition/group/" + str(group['id']))
    
      rounds = json.loads(currSec.text)['rounds']
      for round in rounds:
        matches = round['matches']
        for match in matches:
          winner = 1
          # check for bye
          if ((match['teams'][0] == []) or (match['teams'][1] == [])):
              continue
          player1 = match['teams'][0]['nicename']
          player2 = match['teams'][1]['nicename']
          winner = match['winner']
          matchTable.append([player1, player2, winner])

    return matchTable

# Returns a table of all the matches in data.txt by going through the html (this doesnt currently include top 16).
def createMatchTable(datafile):
    matchTable = []
    nextline = datafile.readline()

    #simple hack, the end of the file will close the html
    while (nextline.find("</html>") == -1):
        #whenever we see a match, this may have to be changed, it is a little sensitive
        if (nextline.find("onClick=") > -1):
            matchTable.append(getMatchEntry(datafile))
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

def fillMatchupMatrixVsLineup(matchupMatrix, playerTable, matchTable):
    for match in matchTable:
        winner = -1
        loser = -1
        if (match[2] == 2):
            winner = 1
            loser = 0
        else:
            winner = 0
            loser = 1

        winLineup = -1
        lossLineup = -1

        for player in playerTable:
            if (match[winner] == player[0]):
                winLineup = player[1]
                print("yay")
            if (match[loser] == player[0]):
                lossLineup = player[1]

        if (winLineup == -1) or (lossLineup == -1):
            #something weird happened, the player decks werent found in the JSON
            continue

        if not (winLineup == lossLineup):
            print("very good")
            matchupMatrix[winLineup][lossLineup][0] += 1
            matchupMatrix[winLineup][lossLineup][1] += 1

            matchupMatrix[lossLineup][winLineup][1] += 1


# Cross-references the playerTable and the matchTable in order to fill out the matchupMatrix.
# matchupMatrix is mutated. playerTable and matchTable are kept constant
def fillMatchupMatrix(matchupMatrix, playerTable, matchTable):
    for match in matchTable:
        winner = -1
        loser = -1
        if (match[2] == 2):
            winner = 1
            loser = 0
        else:
            winner = 0
            loser = 1

        winClass1 = -1
        winClass2 = -1
        lossClass1 = -1
        lossClass2 = -1

        for player in playerTable:
            if (match[winner] == player[0]):
                winClass1 = player[1]
                winClass2 = player[2]
            if (match[loser] == player[0]):
                lossClass1 = player[1]
                lossClass2 = player[2]

        if ((winClass1 == -1) or (winClass2 == -1) or (lossClass1 == -1) or (lossClass2 == -1)):
            #something weird happened, the player decks werent found in the JSON
            continue

        if (not (((winClass1 == lossClass1) and (winClass2 == lossClass2))
            or ((winClass1 == lossClass2) and (winClass2 == lossClass1)))):
            matchupMatrix[winClass1][lossClass1][0] += 1
            matchupMatrix[winClass2][lossClass1][0] += 1
            matchupMatrix[winClass1][lossClass1][1] += 1
            matchupMatrix[winClass2][lossClass1][1] += 1

            matchupMatrix[winClass1][lossClass2][0] += 1
            matchupMatrix[winClass2][lossClass2][0] += 1
            matchupMatrix[winClass1][lossClass2][1] += 1
            matchupMatrix[winClass2][lossClass2][1] += 1

            matchupMatrix[lossClass1][winClass1][1] += 1
            matchupMatrix[lossClass1][winClass2][1] += 1
            matchupMatrix[lossClass2][winClass1][1] += 1
            matchupMatrix[lossClass2][winClass2][1] += 1

# Output links to all the decks used, along with how many wins they got while in the top 16.
def printAllDecks(participants, playerTable):
    top16out = open("top16out.txt", "a+")
    wins = 4
    while (wins > -1):
        top16out.write("Wins: " + str(wins) + "\r\n")
        for player in participants:
            for playr in playerTable:
                if (player['nicename'] == playr[0]):
                    if (playr[3] == wins):
                        for deck in player['sv_decks']:
                            top16out.write(archs[getarch(deck['hash'])][0] + "\r\n")
                            top16out.write("https://shadowverse-portal.com/deck/" + deck['hash'] + "\r\n")
        top16out.write("\r\n")
        wins -= 1

def main():
    # Initiating lists that will be used
    archSetWins = []
    archSetLosses = []
    winrateTable = []
    top16 = []
    matchupMatrix = []

    datafile = open("data.txt", 'r')
    for i in range(numArchs):
        archSetWins.append(0)
        archSetLosses.append(0)
        winrateTable.append([archs[i][0], 0])
        top16.append(0)
        nextrow = []
        #TODO: for lineups
        for j in range(numArchs):
            nextrow.append([0,0])
        #for j in range(len(lineups)):
        #    nextrow.append([0,0])
        matchupMatrix.append(nextrow)

    # Get the json that was pulled
    jsonfile = open("entrylist.txt", 'r')
    data = json.loads(jsonfile.readline())
    jsonfile.close()

    # Get the participants that actually played
    partic = data['data']
    participants = top256(partic)

    # Printing the number of each archetype
    print_arch_selection(participants)

    # Make the table of players, entries are of the form: [Name, Arch1, Arch2, Number of Wins,
    # Number of Losses]
    # After this function call, the Number of Wins and Number of Losses are initially 0
    playerTable = createTable(participants)

    # Make the table of matches, entires are of the form: [Player1, Player2, Winner (either 1 or 2)]
    matchTable = newCreateMatchTable(datafile)

    # Cross-reference playerTable and matchTable to determine the number of wins and losses for each
    # archetype. Also updates the players with the number of wins/losses they achieved.
    crossReference(playerTable, matchTable, archSetWins, archSetLosses)

    # Uses the playerTable and matchTable in order to fill out the matchup matrix.
    # TODO for lineups
    fillMatchupMatrix(matchupMatrix, playerTable, matchTable)
    # fillMatchupMatrixVsLineup(matchupMatrix, playerTable, matchTable)

    for player in playerTable:
        if (player[3] == 4):
            top16[player[1]] += 1
            top16[player[2]] += 1

    for i in range(numArchs):
        if (archSetWins[i] + archSetLosses[i] == 0):
            winrateTable[i][1] = 0
        else:
            winrateTable[i][1] = Fraction(archSetWins[i], archSetWins[i] + archSetLosses[i])

    winrateTable.sort(key = sortSecond)

    # If we are in the top 16, output all the decklists
    if (len(participants) == 16):
      printAllDecks(participants, playerTable)

    print "\nWinrates:"
    for i in range(numArchs):
        print (winrateTable[i][0] + " = " + str(round(float(winrateTable[i][1]),4)))

    print "\nSets won by each archetype: "
    print archSetWins
    print "\nSets lost by each archetype: "
    print archSetLosses
    print "\nNumber of each archetype hitting top 16: "
    print top16
    print "\nMatchup Matrix:"
    matrixfile = open("archmatrix.txt", "a+")
    for i in range(numArchs):
        matrixfile.write(str(matchupMatrix[i]) + "\n")
        print archs[i][0] + ": " + str(matchupMatrix[i])


#main()
