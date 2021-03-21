import random
import pygame

#check if an index is within the matrix
def checkValidIndex(d, row, col):
    return (row >= 0 and row < d) and (col >= 0 and col < d)

def getNeighbors(info, row, col):
    toReturn = []
    d = len(info)

    #northwest
    if checkValidIndex(d, row-1, col-1):
        toReturn.append((row-1, col-1))
    #west
    if checkValidIndex(d, row, col-1):
        toReturn.append((row, col-1))
    #southwest
    if checkValidIndex(d, row+1, col-1):
        toReturn.append((row+1, col-1))
    #north
    if checkValidIndex(d, row-1, col):
        toReturn.append((row-1, col))
    #south
    if checkValidIndex(d, row+1, col):
        toReturn.append((row+1, col))
    #northesat
    if checkValidIndex(d, row-1, col+1):
        toReturn.append((row-1, col+1))
    #east
    if checkValidIndex(d, row, col+1):
        toReturn.append((row, col+1))
    #southeast
    if checkValidIndex(d, row+1, col+1):
        toReturn.append((row+1, col+1))

    return toReturn

#make a matrix of information for each index
def fillInInfo(matrix, d):
    toReturn = []
    for i in range(len(matrix)):
        toAdd = []
        for j in range(len(matrix)):
            dic = {}

            #keep track of whether or not the square has been directly searched yet
            dic["safe"] = "inconclusive"
            dic["status"] = "unqueried"

            #if safe, the number of mines surrounding it indicated by the clue
            dic["clue"] = ""
            if matrix[i][j] == "m":
                dic["clue"] = "m"
            else:
                dic["clue"] = matrix[i][j]

            #the number of safe squares identified around it, and number of mines around. also fill in hidden squares by counting valid squares around index
            dic["revealed_safe"] = 0
            dic["revealed_mines"] = 0
            dic["hidden_neighbors"] = 0
            #northwest
            if checkValidIndex(d, i-1, j-1):
                dic["hidden_neighbors"]+=1
            #west
            if checkValidIndex(d, i, j-1):
                dic["hidden_neighbors"]+=1
            #southwest
            if checkValidIndex(d, i+1, j-1):
                dic["hidden_neighbors"]+=1
            #north
            if checkValidIndex(d, i-1, j):
                dic["hidden_neighbors"]+=1
            #south
            if checkValidIndex(d, i+1, j):
                dic["hidden_neighbors"]+=1
            #northesat
            if checkValidIndex(d, i-1, j+1):
                dic["hidden_neighbors"]+=1
            #east
            if checkValidIndex(d, i, j+1):
                dic["hidden_neighbors"]+=1
            #southeast
            if checkValidIndex(d, i+1, j+1):
                dic["hidden_neighbors"]+=1


            #FOR USE IN ADVANCED AGENT
            dic["mines_set"] = set()
            dic["complete"] = False

            toAdd.append(dic)
        toReturn.append(toAdd)

    return toReturn

#generate a d x d environment with n mines in it.  only places mines, does not put in numbers yet.
def generate(d, n):
    minesRemaining = n
    toReturn = []
    for i in range(d):
        addLine = []
        for j in range(d):
            addLine.append(0)
        toReturn.append(addLine)

    cease = False
    while minesRemaining > 0:
        if cease:
            break
        for i in range(d):
            if cease:
                break
            for j in range(d):
                if toReturn[i][j] != "m" and random.randint(1, 100) <= 5:
                    #fill in mines by chance, update numbers of indices surrounding the mine
                    toReturn[i][j] = "m"
                    #northwest
                    if checkValidIndex(d, i-1, j-1) and toReturn[i-1][j-1] != "m":
                        toReturn[i-1][j-1]+=1
                    #west
                    if checkValidIndex(d, i, j-1) and toReturn[i][j-1] != "m":
                        toReturn[i][j-1]+=1
                    #southwest
                    if checkValidIndex(d, i+1, j-1) and toReturn[i+1][j-1] != "m":
                        toReturn[i+1][j-1]+=1
                    #north
                    if checkValidIndex(d, i-1, j) and toReturn[i-1][j] != "m":
                        toReturn[i-1][j]+=1
                    #south
                    if checkValidIndex(d, i+1, j) and toReturn[i+1][j] != "m":
                        toReturn[i+1][j]+=1
                    #northesat
                    if checkValidIndex(d, i-1, j+1) and toReturn[i-1][j+1] != "m":
                        toReturn[i-1][j+1]+=1
                    #east
                    if checkValidIndex(d, i, j+1) and toReturn[i][j+1] != "m":
                        toReturn[i][j+1]+=1
                    #southeast
                    if checkValidIndex(d, i+1, j+1) and toReturn[i+1][j+1] != "m":
                        toReturn[i+1][j+1]+=1
                    minesRemaining -= 1
                    if minesRemaining == 0:
                        cease = True
                    if cease:
                        break

    return toReturn

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(str(matrix[i][j]) + " ", end='')
        print("\n")
