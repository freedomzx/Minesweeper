from environmentGenerator import *
from collections import deque
import random

def basicagent(matrix, mines):
    #keep track of numbers
    totalQueries = 0
    explosions = 0
    totalCells = len(matrix) * len(matrix)
    flags = 0

    #matrix of dictionaries contraining info for each cell
    info = fillInInfo(matrix, len(matrix))

    #queue for determined safe cells
    safeQueue = deque()

    finished = False
    while not finished:
        nextCell = ()
        if not safeQueue:
            nextCell = findBetterDecision(info)
        else:
            nextCell = safeQueue.pop()

        if nextCell == "done":
            break

        row = nextCell[0]
        col = nextCell[1]
        
        if matrix[row][col] != "m":
            #check if every remaining neighbor is a mine
            if (info[row][col]["clue"] - info[row][col]["revealed_mines"]) == info[row][col]["hidden_neighbors"] and info[row][col]["hidden_neighbors"] != 0:
                neighbors = getNeighbors(info, row, col)
                info[row][col]["hidden_neighbors"] = 0
                #print(str((row, col)) + " has all mines - Hidden Neighbors: " + str(info[row][col]["hidden_neighbors"]) + " - Mines: " + str(info[row][col]["revealed_mines"]) + " - Safe: " + str(info[row][col]["revealed_safe"]) + " - Clue: " + str(info[row][col]["clue"]))
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    #print(str(nrow) + " " + str(ncol))
                    if info[nrow][ncol]["safe"] == "inconclusive" and info[nrow][ncol]["status"] == "unqueried":
                        #print(str((nrow, ncol)) + " flagged as a new mine")
                        info[nrow][ncol]["safe"] = False
                        info[nrow][ncol]["status"] = "flagged"
                        flags += 1
                        totalQueries += 1
                        #info[row][col]["revealed_mines"] += 1
                        #let neighbors know of this change
                        far = getNeighbors(info, nrow, ncol)
                        for f in far:
                            frow = f[0]
                            fcol = f[1]
                            #print(str((frow, fcol)) + " updated for " + str((nrow, ncol)))
                            info[frow][fcol]["hidden_neighbors"] -= 1
                            info[frow][fcol]["revealed_mines"] += 1

            #check if every neighbor is safe
            if (len(getNeighbors(info, row, col)) - info[row][col]["clue"] - info[row][col]["revealed_safe"]) == info[row][col]["hidden_neighbors"] and info[row][col]["hidden_neighbors"] != 0:
                neighbors = getNeighbors(info, row, col)
                info[row][col]["hidden_neighbors"] = 0
                #print(str((row, col)) + " has all safe - Hidden Neighbors: " + str(info[row][col]["hidden_neighbors"]) + " - Mines: " + str(info[row][col]["revealed_mines"]) + " - Safe: " + str(info[row][col]["revealed_safe"]) + " - Clue: " + str(info[row][col]["clue"]))
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    if info[nrow][ncol]["safe"] == "inconclusive" and info[nrow][ncol]["status"] == "unqueried":
                        #print(str((nrow, ncol)) + " flagged as a new safe")
                        info[nrow][ncol]["safe"] = True
                        info[nrow][ncol]["status"] = "in queue"
                        safeQueue.append((nrow, ncol))
                        #info[row][col]["revealed_safe"] += 1
                        #let neighbors know new safe
                        far = getNeighbors(info, nrow, ncol) 
                        for f in far:
                            frow = f[0]
                            fcol = f[1]
                            #print(str((frow, fcol)) + " updated for " + str((nrow, ncol)))
                            info[frow][fcol]["hidden_neighbors"] -= 1
                            info[frow][fcol]["revealed_safe"] += 1

        if matrix[row][col] == "m":
            #print(str((row, col)) + "exploded")
            info[row][col]["safe"] = False
            info[row][col]["status"] = "queried"
            explosions += 1
            totalQueries += 1
            neighbors = getNeighbors(info, row, col)
            for n in neighbors:
                nrow = n[0]
                ncol = n[1]
                #print(str((nrow, ncol)) + " updated for boom", end = ' ')
                info[nrow][ncol]["hidden_neighbors"] -= 1
                info[nrow][ncol]["revealed_mines"] += 1
            #print("\n")

        else:
            #print(str((row, col)) + " was safe")
            wasQueried = False
            if info[row][col]["status"] == "in queue":
                wasQueried = True
            info[row][col]["safe"] = True
            info[row][col]["status"] = "queried"
            totalQueries += 1

            if not wasQueried:
                neighbors = getNeighbors(info, row, col)
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    #print(str((nrow, ncol)) + " updated for safe", end = ' ')
                    info[nrow][ncol]["hidden_neighbors"] -= 1
                    info[nrow][ncol]["revealed_safe"] += 1
                #print("\n")
                    

    #print("Success rate: " + str(flags / mines) + "\nExplosions: " + str(explosions) + "\nFlags: " + str(flags) + "\nTotal Queries: " + str(totalQueries))
    return (flags / mines)

#returns a random hidden cell
def findRandomHidden(info):
    randomList = []
    for i in range(len(info)):
        for j in range(len(info)):
            if info[i][j]["safe"] == "inconclusive" and info[i][j]["status"] == "unqueried":
                randomList.append((i, j))

    if not randomList:
        #print("returned done")
        return "done"

    else:
        num = random.randint(0, len(randomList)-1)
        #print("returned" + " " + str(randomList[num]))
        #print(info[randomList[num][0]][randomList[num][1]])
        return randomList[num]

def findBetterDecision(info): 
    smallestChance = 1.0
    bestCoord = ()
    listCoord = []
    maxNum = 0
    #for the infor matrix, find the dictionary that has the smallest surrounding clue mines attribute, 
    for i in range(len(info)):
        for j in range(len(info)):
            #when the surrounding clued mines is at 0, it would be the smallest, which we can just return the neighbor of the cell
            if info[i][j]["clue"] == 0:
                listCoord = getNeighbors(info, i, j)
                for coordinate in listCoord:
                    if info[coordinate[0]][coordinate[1]]["status"] == "unqueried" and info[coordinate[0]][coordinate[1]]["safe"] == "inconclusive":
                        return coordinate

            #find coordinate with smallest chance of picking random neighbor = mine
            elif type(info[i][j]["clue"]) is int and info[i][j]["hidden_neighbors"] > info[i][j]["clue"]:
                remaining_mines = info[i][j]["clue"] - info[i][j]["revealed_mines"]
                chance = float(remaining_mines / info[i][j]["hidden_neighbors"])
                if chance < smallestChance:
                    smallestChance = chance
                    bestCoord = (i, j)

    if smallestChance == 1.0:
        return findRandomHidden(info)

    else:
        neighbors = getNeighbors(info, bestCoord[0], bestCoord[1])
        randomIndex = random.randint(0, len(neighbors)-1)
        return neighbors[randomIndex]



            