from environmentGenerator import *
from minesweeper import *
from collections import deque
import random

def basicagent(matrix, n):
    #keep track of numbers
    totalQueries = 0
    explosions = 0
    goodQueries = 0
    totalCells = len(matrix) * len(matrix)

    #matrix of dictionaries contraining info for each cell
    info = fillInInfo(matrix, len(matrix))
    d = len(matrix)

    #queue for determined safe cells
    safeQueue = deque()

    finished = False
    while not finished:
        nextCell = ()
        if not safeQueue:
            nextCell = findRandomHidden(info)
        else:
            nextCell = safeQueue.pop()

        row = nextCell[0]
        col = nextCell[1]

        #check if we need to make all neighbors safe/flag all neighbors as mines, increment totalQueries or push into safeQueue as necessary
        if info[row][col]["surrounding_clued_mines"] - info[row][col]["surrounding_mines"] == info[row][col]["surrounding_hidden_squares"]:
            #northwest
            if checkValidIndex(d, row-1, col-1) and info[row-1][col-1]["status"] == "unqueried":
                info[row-1][col-1]["safe"] = False
                info[row-1][col-1]["status"] = "flagged"
                totalQueries += 1
            #west
            if checkValidIndex(d, row, col-1) and info[row][col-1]["status"] == "unqueried":
                info[row][col-1]["safe"] = False
                info[row][col-1]["status"] = "flagged"
                totalQueries += 1
            #southwest
            if checkValidIndex(d, row+1, col-1) and info[row+1][col-1]["status"] == "unqueried":
                info[row+1][col-1]["safe"] = False
                info[row+1][col-1]["status"] = "flagged"
                totalQueries += 1
            #north
            if checkValidIndex(d, row-1, col) and info[row-1][col]["status"] == "unqueried":
                info[row-1][col]["safe"] = False
                info[row-1][col]["status"] = "flagged"
                totalQueries += 1
            #south
            if checkValidIndex(d, row+1, col) and info[row+1][col]["status"] == "unqueried":
                info[row+1][col]["safe"] = False
                info[row+1][col]["status"] = "flagged"
                totalQueries += 1
            #northesat
            if checkValidIndex(d, row-1, col+1) and info[row-1][col+1]["status"] == "unqueried":
                info[row-1][col+1]["safe"] = False
                info[row-1][col+1]["status"] = "flagged"
                totalQueries += 1
            #east
            if checkValidIndex(d, row, col+1) and info[row][col+1]["status"] == "unqueried":
                info[row][col+1]["safe"] = False
                info[row][col+1]["status"] = "flagged"
                totalQueries += 1
            #southeast
            if checkValidIndex(d, row+1, col+1) and info[row+1][col+1]["status"] == "unqueried":
                info[row+1][col+1]["safe"] = False
                info[row+1][col+1]["status"] = "flagged"
                totalQueries += 1
        elif (8 - info[row][col]["surrounding_clued_mines"]) - info[row][col]["surrounding_safe_squares"] == info[row][col]["surrounding_hidden_squares"]:
            #northwest
            if checkValidIndex(d, row-1, col-1) and info[row-1][col-1]["status"] == "unqueried":
                info[row-1][col-1]["safe"] = True
                safeQueue.append((row-1, col-1))
            #west
            if checkValidIndex(d, row, col-1) and info[row][col-1]["status"] == "unqueried":
                info[row][col-1]["safe"] = True
                safeQueue.append((row, col-1))
            #southwest
            if checkValidIndex(d, row+1, col-1) and info[row+1][col-1]["status"] == "unqueried":
                info[row+1][col-1]["safe"] = True
                safeQueue.append((row+1, col-1))
            #north
            if checkValidIndex(d, row-1, col) and info[row-1][col]["status"] == "unqueried":
                info[row-1][col]["safe"] = True
                safeQueue.append((row-1, col))
            #south
            if checkValidIndex(d, row+1, col) and info[row+1][col]["status"] == "unqueried":
                info[row+1][col]["safe"] = True
                safeQueue.append((row+1, col))
            #northesat
            if checkValidIndex(d, row-1, col+1) and info[row-1][col+1]["status"] == "unqueried":
                info[row-1][col+1]["safe"] = True
                safeQueue.append((row-1, col+1))
            #east
            if checkValidIndex(d, row, col+1) and info[row][col+1]["status"] == "unqueried":
                info[row][col+1]["safe"] = True
                safeQueue.append((row, col+1))
            #southeast
            if checkValidIndex(d, row+1, col+1) and info[row+1][col+1]["status"] == "unqueried":
                info[row+1][col+1]["safe"] = True
                safeQueue.append((row+1, col+1))

        #boom
        if matrix[row][col] == "m":
            explosions += 1
            info[row][col]["status"] = "queried"
            #northwest
            if checkValidIndex(d, row-1, col-1):
                info[row-1][col-1]["surrounding_hidden_squares"]-=1
                info[row-1][col-1]["surrounding_mines"]+=1
            #west
            if checkValidIndex(d, row, col-1):
                info[row][col-1]["surrounding_hidden_squares"]-=1
                info[row][col-1]["surrounding_mines"]+=1
            #southwest
            if checkValidIndex(d, row+1, col-1):
                info[row+1][col-1]["surrounding_hidden_squares"]-=1
                info[row+1][col-1]["surrounding_mines"]+=1
            #north
            if checkValidIndex(d, row-1, col):
                info[row-1][col]["surrounding_hidden_squares"]-=1
                info[row-1][col]["surrounding_mines"]+=1
            #south
            if checkValidIndex(d, row+1, col):
                info[row+1][col]["surrounding_hidden_squares"]-=1
                info[row+1][col]["surrounding_mines"]+=1
            #northeast
            if checkValidIndex(d, row-1, col+1):
                info[row-1][col+1]["surrounding_hidden_squares"]-=1
                info[row-1][col+1]["surrounding_mines"]+=1
            #east
            if checkValidIndex(d, row, col+1):
                info[row][col+1]["surrounding_hidden_squares"]-=1
                info[row][col+1]["surrounding_mines"]+=1
            #southeast
            if checkValidIndex(d, row+1, col+1):
                info[row+1][col+1]["surrounding_hidden_squares"]-=1
                info[row+1][col+1]["surrounding_mines"]+=1

        #good query
        else:
            goodQueries += 1
            info[row][col]["status"] = "queried"
            #northwest
            if checkValidIndex(d, row-1, col-1):
                info[row-1][col-1]["surrounding_hidden_squares"]-=1
                info[row-1][col-1]["surrounding_squares"]+=1
            #west
            if checkValidIndex(d, row, col-1):
                info[row][col-1]["surrounding_hidden_squares"]-=1
                info[row][col-1]["surrounding_safe_squares"]+=1
            #southwest
            if checkValidIndex(d, row+1, col-1):
                info[row+1][col-1]["surrounding_hidden_squares"]-=1
                info[row+1][col-1]["surrounding_safe_squares"]+=1
            #north
            if checkValidIndex(d, row-1, col):
                info[row-1][col]["surrounding_hidden_squares"]-=1
                info[row-1][col]["surrounding_safe_squares"]+=1
            #south
            if checkValidIndex(d, row+1, col):
                info[row+1][col]["surrounding_hidden_squares"]-=1
                info[row+1][col]["surrounding_safe_squares"]+=1
            #northeast
            if checkValidIndex(d, row-1, col+1):
                info[row-1][col+1]["surrounding_hidden_squares"]-=1
                info[row-1][col+1]["surrounding_safe_squares"]+=1
            #east
            if checkValidIndex(d, row, col+1):
                info[row][col+1]["surrounding_hidden_squares"]-=1
                info[row][col+1]["surrounding_safe_squares"]+=1
            #southeast
            if checkValidIndex(d, row+1, col+1):
                info[row+1][col+1]["surrounding_hidden_squares"]-=1
                info[row+1][col+1]["surrounding_safe_squares"]+=1

        #we're done here
        if totalQueries == totalCells:
            break
        
    print(goodQueries / totalQueries)

#returns a random hidden cell
def findRandomHidden(info):
    randomList = []
    for i in range(len(info)):
        for j in range(len(info)):
            if info[i][j]["safe"] == "inconclusive" and info[i][j]["status"] == "unqueried":
                randomList.append((i, j))

    if not randomList:
        return "done"

    else:
        num = random.randint(0, len(randomList)-1)
        return randomList[num]
    



