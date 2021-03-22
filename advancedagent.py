from environmentGenerator import *
from collections import deque
import random



def advancedagent(matrix, mines):
    #keep track of numbers
    #totalQueries = 0
    explosions = 0
    totalCells = len(matrix) * len(matrix)
    #flags = 0
    nums = {}
    nums["totalQueries"] = 0
    nums["flags"] = 0

    #matrix of dictionaries contraining info for each cell
    info = fillInInfo(matrix, len(matrix))

    #queue for determined safe cells
    safeQueue = deque()

    #advanced agent main topic. use list of equations to see if we can infer any new mines with new info
    equations = []
    for i in range(len(matrix)):
        toAdd = []
        for j in range(len(matrix)):
            dic = {}
            #keep track of equations and remaining unknown mines for everycell (only the non-mines are important though)
            dic["coordinates"] = (i ,j)
            dic["num_unknown"] = matrix[i][j]
            dic["potential_mines"] = set()
            dic["complete"] = False
            toAdd.append(dic)
        equations.append(toAdd)

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
                        nums["flags"] += 1
                        nums["totalQueries"] += 1
                        #info[row][col]["revealed_mines"] += 1

                        #ADVANCED: LET NEIGHBORS KNOW NEW MINE
                        removeMineCoordinate(info, equations, nrow, ncol)

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

                        #ADVANCED: LET NEIGHBORS KNOW NEW SAFE
                        removeSafeCoordinate(info, equations, nrow, ncol)

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
            nums["totalQueries"] += 1
            neighbors = getNeighbors(info, row, col)
            for n in neighbors:
                nrow = n[0]
                ncol = n[1]
                #print(str((nrow, ncol)) + " updated for boom", end = ' ')
                info[nrow][ncol]["hidden_neighbors"] -= 1
                info[nrow][ncol]["revealed_mines"] += 1
            #print("\n")

            #ADVANCED: LET NEIGHBORS KNOW A MINE HAS BEEN FOUND
            removeMineCoordinate(info, equations, row, col)

        else:
            #print(str((row, col)) + " was safe")
            wasQueried = False
            if info[row][col]["status"] == "in queue":
                wasQueried = True
            info[row][col]["safe"] = True
            info[row][col]["status"] = "queried"
            nums["totalQueries"] += 1

            #update neighbors if not already done
            if not wasQueried:
                neighbors = getNeighbors(info, row, col)
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    #print(str((nrow, ncol)) + " updated for safe", end = ' ')
                    info[nrow][ncol]["hidden_neighbors"] -= 1
                    info[nrow][ncol]["revealed_safe"] += 1
                #print("\n")

            #ADVANCED: ENTER POTENTIAL MINE NEIGHBORS
            if info[row][col]["clue"] > 0:
                neighbors = getNeighbors(info, row, col)
                for n in neighbors:
                    nrow = n[0]
                    ncol = n[1]
                    equations[row][col]["potential_mines"].add((nrow, ncol))

            #ADVANCED: REMOVE THIS COORDINATE FROM ANY MINE'S "POTENTIAL MINES" SET
            removeSafeCoordinate(info, equations, row, col)

        #ADVANCED: assess equations
        assess(info, equations, safeQueue, nums)

    print("Success rate: " + str(nums["flags"] / mines) + "\nExplosions: " + str(explosions) + "\nFlags: " + str(nums["flags"]) + "\nTotal Queries: " + str(nums["totalQueries"]))
    return (nums["flags"] / mines)

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
        return randomList[num]

#remove a safe coordinate from equations
def removeSafeCoordinate(info, equations, row, col):
    neighbors = getNeighbors(info, row, col)
    for n in neighbors:
        nrow = n[0]
        ncol = n[1]
        equations[nrow][ncol]["potential_mines"].discard((row, col))

#remove a mine coordinate from equations
def removeMineCoordinate(info, equations, row, col):
    neighbors = getNeighbors(info, row, col)
    for n in neighbors:
        nrow = n[0]
        ncol = n[1]
        if (row, col) in equations[nrow][ncol]["potential_mines"]:
            equations[nrow][ncol]["potential_mines"].discard((row, col))
            equations[nrow][ncol]["num_unknown"] -= 1

#remove safe coordiante except for a certain one
def removeSafeExcept(info, equations, row, col, erow, ecol):
    neighbors = getNeighbors(info, row, col)
    for n in neighbors:
        nrow = n[0]
        ncol = n[1]
        if nrow == erow and ncol == ecol:
            continue
        equations[nrow][ncol]["potential_mines"].discard((row, col))

#remove mine coordinate except for a certain one
def removeMineExcept(info, equations, row, col, erow, ecol):
    neighbors = getNeighbors(info, row, col)
    for n in neighbors:
        nrow = n[0]
        ncol = n[1]
        if nrow == erow and ncol == ecol:
            continue
        if (row, col) in equations[nrow][ncol]["potential_mines"]:
            equations[nrow][ncol]["potential_mines"].discard((row, col))
            equations[nrow][ncol]["num_unknown"] -= 1

#try to find new safe cells given what we have in equations
def assess(info, equations, safeQueue, nums):
    for i in range(len(info)):
        for j in range(len(info)):
            if not equations[i][j]["complete"] and equations[i][j]["num_unknown"] != "m":
                #check if num_unknown = 0, if so, then everything still left under potential_mines is good to go (safe)
                if equations[i][j]["num_unknown"] == 0:
                    equations[i][j]["complete"] = True
                    for cell in equations[i][j]["potential_mines"]:
                        crow = cell[0]
                        ccol = cell[1]

                        if info[crow][ccol]["safe"] == "inconclusive" and info[crow][ccol]["status"] == "unqueried":
                            #info[i][j]["revealed_safe"] += 1
                            info[crow][ccol]["safe"] = True
                            info[crow][ccol]["status"] = "in queue"
                            safeQueue.append((crow, ccol))
                            #print("good job!")

                            removeSafeExcept(info, equations, crow, ccol, i, j)

                            #let neighbors know
                            far = getNeighbors(info, crow, ccol)
                            for f in far:
                                frow = f[0]
                                fcol = f[1]
                                info[frow][fcol]["hidden_neighbors"] -= 1
                                info[frow][fcol]["revealed_safe"] += 1

                #check if length of potential_mines == num_unknown, means that everything there is a mine
                elif equations[i][j]["num_unknown"] == len(equations[i][j]["potential_mines"]):
                    equations[i][j]["complete"] = True
                    for cell in equations[i][j]["potential_mines"]:
                        crow = cell[0]
                        ccol = cell[1]

                        if info[crow][ccol]["safe"] == "inconclusive" and info[crow][ccol]["status"] == "unqueried":
                            info[crow][ccol]["safe"] = False
                            info[crow][ccol]["status"] = "flagged"
                            nums["flags"] += 1
                            nums["totalQueries"] += 1
                            #print("good job!")

                            removeMineExcept(info, equations, crow, ccol, i, j)

                            #let neighbors know
                            far = getNeighbors(info, crow, ccol)
                            for f in far:
                                frow = f[0]
                                fcol = f[1]
                                info[frow][fcol]["hidden_neighbors"] -= 1
                                info[frow][fcol]["revealed_mines"] += 1





            