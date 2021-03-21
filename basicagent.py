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
            nextCell = findRandomHidden(info)
        else:
            nextCell = safeQueue.pop()

        if nextCell == "done":
            break

        row = nextCell[0]
        col = nextCell[1]
        
        if matrix[row][col] != "m":
            #check if every remaining neighbor is a mine
            if (info[row][col]["clue"] - info[row][col]["revealed_mines"]) == info[row][col]["hidden_neighbors"]:
                neighbors = getNeighbors(info, row, col)
                print(str((row, col)) + " has all mines - Hidden Neighbors: " + str(info[row][col]["hidden_neighbors"]) + " Mines: " + str(info[row][col]["revealed_mines"]) + " Safe: " + str(info[row][col]["revealed_safe"]))
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    #print(str(nrow) + " " + str(ncol))
                    if info[nrow][ncol]["safe"] == "inconclusive" and info[nrow][ncol]["status"] == "unqueried":
                        info[nrow][ncol]["safe"] = False
                        info[nrow][ncol]["status"] = "flagged"
                        flags += 1
                        totalQueries += 1
                        #let neighbors know of this change
                        far = getNeighbors(info, nrow, ncol)
                        for f in far:
                            frow = f[0]
                            fcol = f[1]
                            info[frow][fcol]["hidden_neighbors"] -= 1
                            info[frow][fcol]["revealed_mines"] += 1

            #check if every neighbor is safe
            if (len(getNeighbors(info, row, col)) - info[row][col]["clue"] - info[row][col]["revealed_safe"]) == info[row][col]["hidden_neighbors"]:
                neighbors = getNeighbors(info, row, col)
                print(str((row, col)) + " has all safe - Hidden Neighbors: " + str(info[row][col]["hidden_neighbors"]) + " Mines: " + str(info[row][col]["revealed_mines"]) + " Safe: " + str(info[row][col]["revealed_safe"]))
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    if info[nrow][ncol]["safe"] == "inconclusive" and info[nrow][ncol]["status"] == "unqueried":
                        info[nrow][ncol]["safe"] = True
                        info[nrow][ncol]["status"] = "in queue"
                        safeQueue.append((nrow, ncol))
                        #let neighbors know new safe
                        far = getNeighbors(info, nrow, ncol) 
                        for f in far:
                            frow = f[0]
                            fcol = f[1]
                            info[frow][fcol]["hidden_neighbors"] -= 1
                            info[frow][fcol]["revealed_safe"] += 1

        if matrix[row][col] == "m":
            info[row][col]["safe"] = False
            info[row][col]["status"] = "queried"
            explosions += 1
            totalQueries += 1
            neighbors = getNeighbors(info, row, col)
            for n in neighbors:
                nrow = n[0]
                ncol = n[1]
                info[nrow][ncol]["hidden_neighbors"] -= 1
                info[nrow][ncol]["revealed_mines"] += 1

        else:
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
                    info[nrow][ncol]["hidden_neighbors"] -= 1
                    info[nrow][ncol]["revealed_safe"] += 1
                    

    print("Success rate: " + str(flags / mines) + "\nExplosions: " + str(explosions) + "\nFlags: " + str(flags) + "\nTotal Queries: " + str(totalQueries))
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
    